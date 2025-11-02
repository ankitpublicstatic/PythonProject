from sympy.physics.units import temperature
from transformers.utils.import_utils import candidates

from extractors import load_all
from retriever import build_vector_index, build_bm25_index, retrieve
from reranker import cross_rerank
from config import PG_CONFIG
from langchain.llms import OpenAI

def build_multi_rag():
    print("🔍 Loading data from all sources...")
    docs = load_all(PG_CONFIG)
    print(f"Loaded {len(docs)} documents")

    print("⚙️ Building retrievers...")
    vector_index, chunks = build_vector_index(docs)
    bm25 = build_bm25_index(chunks)
    return vector_index, bm25, chunks

def query_multi_rag(query, vector_index, bm25, chunks, top_k=20):
    print(f"🧠 Query: {query}")
    candidates = retrieve(query, vector_index, bm25, chunks, top_k)
    reranked = cross_rerank(query,candidates)[:5]
    context = "\n\n---\n\n".join([d.page_content for d in reranked])

    prompt = f""" 

You are an expert assistant. Use only the context to answer accurately. 

Context:{context}
Question: {query}

"""
    llm = OpenAI(temperature = 0)
    answer = llm(prompt)
    return answer

if __name__ == "__main__":
    vector_index, bm25, chunks = build_multi_rag()
    print(query_multi_rag("Expalin microservices communication patterns", vector_index, bm25, chunks))


"""
🧮 How It Works

Document extraction:

PDFs → parsed with pdfplumber

HTML → cleaned via BeautifulSoup

Code → raw text ingestion

PostgreSQL → SQL query → text documents

Chunking:
Documents are split into ~512-token chunks with overlap.

Embeddings + Storage:

Embeddings = OpenAIEmbeddings()

Stored in Pinecone vector index

Retrieval:

Retrieve from both Pinecone (semantic) and BM25 (keyword).

Merge results (fusion retrieval).

Reranking:

Cross-encoder ranks candidates more accurately.

LLM Response:

Top 5 chunks passed to LLM (OpenAI GPT model) to generate the final grounded answer.
"""