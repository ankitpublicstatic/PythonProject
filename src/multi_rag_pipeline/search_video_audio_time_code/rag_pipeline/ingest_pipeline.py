
# pip install boto3 scenedetect sentence-transformers qdrant-client openai psycopg2-binary ffmpeg-python
# optionally: pip install openai-whisper or use whisper.cpp bindings for performance (or use AWS Transcribe)


import os, io, uuid, json, tempfile, subprocess
from pathlib import Path
import boto3
import psycopg2
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
import openai

# CONFIG (env)
S3_BUCKET = os.environ['S3_BUCKET']
QDRANT_HOST = os.environ.get('QDRANT_HOST','localhost')
QDRANT_PORT = int(os.environ.get('QDRANT_PORT','6333'))
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
POSTGRES_DSN = os.environ['POSTGRES_DSN']

openai.api_key =  os.environ.get("OPENAI_API_KEY")

s3 = boto3.client('s3')
qdrant = QdrantClient(url=f'http://{QDRANT_HOST}:{QDRANT_PORT}')
sbert = SentenceTransformer('all-mpnet-base-v2')  # high-quality text embeddings

def download_from_s3(s3_key, local_path):
    s3.download_file(S3_BUCKET, s3_key, local_path)
    return local_path

def detect_scenes(video_path):
    vm = VideoManager([video_path])
    sm = SceneManager()
    sm.add_detector(ContentDetector())
    vm.set_downscale_factor()
    vm.start()
    scene_list = sm.detect_scenes(frame_source=vm)
    vm.release()
    # scene_list: list of (start, end) timecodes
    scenes_ms = []
    for st, end in scene_list:
        scenes_ms.append((int(st.get_seconds()*1000), int(end.get_seconds()*1000)))
    return scenes_ms

def extract_audio(video_path, out_wav):
    # using ffmpeg (ffmpeg must be available in worker)
    subprocess.check_call(['ffmpeg','-i',video_path,'-vn','-ac','1','-ar','16000','-f','wav', out_wav, '-y'])

def transcribe_whisper(wav_path):
    # either call OpenAI api or local whisper. Minimal example using OpenAI transcription endpoint:
    with open(wav_path,'rb') as f:
        resp = openai.Audio.transcriptions.create(file=f, model='whisper-1')
    # The API returns a string text; chunking/timecodes require local whisper with diarization or third-party ASR
    return resp['text']

def compute_text_embeddings(texts):
    # batched
    embs = sbert.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return embs

def create_or_update_collection(collection_name, dim):
    try:
        qdrant.get_collection(collection_name=collection_name)
    except Exception:
        qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config=qmodels.VectorParams(size=dim, distance=qmodels.Distance.COSINE)
        )

def upsert_vectors(collection_name, points):
    # points: list of dict {id, vector, payload}
    qdrant.upsert(collection_name=collection_name, points=points)

def persist_segment_and_metadata(pg_conn, asset_id, seg):
    # seg = dict(start_ms, end_ms, text, attributes)
    with pg_conn.cursor() as cur:
        cur.execute("""
          INSERT INTO segments (id, asset_id, start_ms, end_ms, segment_type, text, thumbnail_uri, attributes)
          VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
          ON CONFLICT (id) DO UPDATE SET text=EXCLUDED.text, attributes=EXCLUDED.attributes
        """,(seg['id'], asset_id, seg['start_ms'], seg['end_ms'], seg['segment_type'], seg.get('text'), seg.get('thumbnail_uri'), json.dumps(seg.get('attributes',{}))))
    pg_conn.commit()

def process_asset(s3_key, asset_id, tenant_id):
    tmp = tempfile.mkdtemp()
    local_video = os.path.join(tmp, 'media.mp4')
    download_from_s3(s3_key, local_video)

    scenes = detect_scenes(local_video)
    audio_wav = os.path.join(tmp,'audio.wav')
    extract_audio(local_video, audio_wav)
    full_transcript = transcribe_whisper(audio_wav)

    # naive segmentation: split transcript per scene; for production do forced-alignment to timecodes
    pg = psycopg2.connect(POSTGRES_DSN)
    collection = f"segments_{tenant_id}"
    # text embedding dim from model
    dummy = sbert.encode("hello")
    create_or_update_collection(collection, dim=len(dummy))

    segments_points = []
    for i,(st,ed) in enumerate(scenes):
        segid = str(uuid.uuid4())
        # create short text summary: for prototype reuse transcript slice; production: forced-alignment, speaker diarization
        seg_text = f"Scene {i} approx {st}-{ed} ms. Transcript excerpt: {full_transcript[:240]}"
        emb = compute_text_embeddings([seg_text])[0].tolist()
        payload = {
            'segment_id': segid,
            'asset_id': asset_id,
            'start_ms': st,
            'end_ms': ed,
            'tenant_id': str(tenant_id),
            'segment_type': 'shot'
        }
        segments_points.append(qmodels.PointStruct(id=segid, vector=emb, payload=payload))

        seg = {
            'id': segid,
            'asset_id': asset_id,
            'start_ms': st,
            'end_ms': ed,
            'segment_type': 'shot',
            'text': seg_text,
            'attributes': {}
        }
        persist_segment_and_metadata(pg, asset_id, seg)

    # upsert to qdrant
    upsert_vectors(collection, segments_points)
    pg.close()
    return {"status":"ok", "ingested_segments": len(segments_points)}
