import os

import cv2
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid


# Qdrant Vector DB Configuration
QDRANT_HOST = os.environ.get('QDRANT_HOST','localhost')
QDRANT_PORT = int(os.environ.get('QDRANT_PORT','6333'))
COLLECTION_NAME = os.environ.get("COLLECTION_NAME")
MODEL_ID = os.environ.get("MODEL_ID")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Initializing AI Model {MODEL_ID} on device {DEVICE}")
clip_model = CLIPModel.from_pretrained(MODEL_ID).to(DEVICE)
clip_processor = CLIPProcessor.from_pretrained(MODEL_ID)

print(f"Connecting to Qdrant on {QDRANT_HOST}:{QDRANT_PORT}....")
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Vector DB Dimensions: 2048, 1024, 768, 512, 384
# Ensure collection exists
try:
    qdrant.get_collection(COLLECTION_NAME)
except Exception:
    print(f"Creating collection {COLLECTION_NAME}...")
    qdrant.create_collection(collection_name=COLLECTION_NAME,
                             vectors_config=models.VectorParams(size=512,
                             distance=models.Distance.COSINE))

def process_and_index_video(file_path:str, asset_metadata: dict):
    """
    Read a video, extract frames at 1fps, generate embeddings,
    and attaches structured metadata before indexing in Qdrant.
    :param file_path:
    :param asset_metadata:
    :return:
    """
    asset_id = asset_metadata.get("asset_id")
    print(f"Processing asset: {asset_id} from {file_path}")

    cap = cv2.VideoCapture(file_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print("Error reading video file.")
        return

    batch_points = []
    frame_interval = int(fps) # Extract 1 frame per second
    frame_counter = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_counter % frame_interval == 0:
            timestamp_seconds = frame_counter / fps

            # 1. Process Image for CLIP
            # Convert BGR (OpenCV default) to RGB

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)

            # 2. Generate Embeddings

            with torch.no_grad():
                inputs = clip_processor(images=pil_image, return_tensors="pt",
                                        padding=True).to(DEVICE)
                image_features = clip_model.get_image_features(**inputs)

                # Normalize for Cosine similarity
                image_features /= image_features.norm(dim=-1, keepdim=True)
                vector = image_features.cpu().float().numpy()[0].tolist()

            # 3. Prepare Hybrid Payload (Semantic Time + Structured Metadata)
            # We denormalize metadata onto every frame for fast filtering.

            payload = {
                "asset_id": asset_id,
                "timestamp": timestamp_seconds,
                "media_type": "video_frame",

                # Structured Fields for filtering later
                "category": asset_metadata.get("category"),
                "project": asset_metadata.get("project"),
                "drm_status": asset_metadata.get("drm_status")
            }

            # Create a Unique ID for this specific segment point
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, name=f"{asset_id}_{timestamp_seconds}"))

            batch_points.append(models.PointStruct(id=point_id,
                                                   vector=vector,
                                                   payload=payload))

            frame_counter += 1

            # Upsert in batches of 50 frames to avoid overloading network
            if len(batch_points) >= 50:
                qdrant.upsert(collection_name=COLLECTION_NAME,points=batch_points)
                batch_points = []
                print("Upserted batch of 50 points to Qdrant.")

        cap.release()

        # Final batch upsert

        if batch_points:
            qdrant.upsert(collection_name=COLLECTION_NAME,points=batch_points)
            print("Upserted final batch to Qdrant.")
        print(f"Finished processing {asset_id}")


# Main Execution Stub (Simulation of an SQS Event processor)

if __name__ == "__main__":
    # Simulate receiving an event to process a new video asset
    # In reality, this metadata comes from RDS/PostgreSQL

    mock_asset_metadata = {
        "asset_id": "video-soccer-final-001",
        "category": "sports",
        "project": "inter_milan_campaign",
        "drm_status": "licensed"
    }

    # Ensure you have a dummy video file name test_video.mp4 in the same directory
    # Or replace path with an actual video file path.
    video_path = "test_video.mp4"

    try:
        # Create dumpy file if not exists for testing
        open(video_path, 'a').close()
        print("Starting ingestion process...")
        # NOTE: To run this actually, provide a real video path.
        # process_and_index_video(video_path, mock_asset_metadata)
        print("Ingestion process finished (Simulated as no real video provided).")
    except Exception as e:
        print(f"An error occurred: {e}")

