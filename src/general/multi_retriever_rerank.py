from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, util
from langchain.llms import OpenAI
from langchain.schema import Document
from sympy.physics.units import temperature

# 1) Ingest & Chunk
loader = TextLoader("docs/mydoc.txt")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=80)
chunks = splitter.split_documents(docs)

# 2) Embeddings & FAISS (Vector store)
embeddings = OpenAIEmbeddings()
faiss_index = FAISS.from_documents(chunks, embeddings=embeddings)


# 3) Build BM25 index (on raw text)
tokenized = [d.page_content.split() for d in chunks]
bm25 = BM25Okapi(tokenized)

# 4) Cross-encoder for reranking
cross_encoder = SentenceTransformer('cross-encoder/ms-marco-MiniLM-L-6-v2')

def multi_retrieve(query: str, top_k: int = 20, top_n: int = 5):
    # Vector results
    vec_docs = faiss_index.similarity_search(query, k=top_k) # returns Document Objects
    # BM25 results
    tokenized_query = query.split()
    bm25_scores= bm25.get_scores(tokenized_query)
    bm25_top_idx = sorted(range(len(bm25_scores)), key=lambda i: -bm25_scores[i])[:top_k]
    bm25_docs = [chunks[i] for i in bm25_top_idx]

    # Merge unique docs (use doc.text to dedup

    candidates = {}
    for d in vec_docs + bm25_docs:
        candidates[d.metadata.get("chunk_id", id(d))] = d

    candidates_list = list(candidates.values())

    # Rerank with cross-encoder
    texts = [d.page_content for d in candidates_list]
    q_and_text = [[query, t] for t in texts]
    rerank_scores = cross_encoder.predict(q_and_text)

    # pair and sort
    paired = sorted(zip(rerank_scores, candidates_list), key=lambda x: -x[0])
    return [doc for score, doc in paired[:top_n]]

# 5) Build prompt and call LLM

llm = OpenAI(temperature =0)

def answer_query(query:str):
    docs_for_prompt = multi_retrieve(query, top_k=50, top_n=5)
    context = "\n\n---\n\n".join([d.page_content for d in docs_for_prompt])
    prompt = f"You are an assistant. Use only the context below to answer the question.\n\nContext:\n{context}\n\nQuestions: {query}\nAnswer with short, precise steps and cite sources."
    return llm(prompt)

print(answer_query("How to implement OAuth2 in spring Boot?"))