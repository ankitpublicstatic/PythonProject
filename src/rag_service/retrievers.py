import asyncio
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from rank_bm25 import BM25Okapi
from transformers.utils.import_utils import candidates

from reranker import cross_rerank

# Preload vectorstore and bm25 index at startup
loader = TextLoader("data/docs/knowledge.txt")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
chunks = splitter.split_documents(docs)

embeddings = OpenAIEmbeddings()
faiss_index = FAISS.from_documents(chunks, embeddings)

tokenized = [d.page_content.split() for d in chunks]
bm25 = BM25Okapi(tokenized)

async def multi_retrieve(query, top_k=30, top_n=5):
    vec_docs = faiss_index.similarity_search(query, k=top_k)
    bm25_scores = bm25.get_scores(query.split())
    bm25_top_idx = sorted(range(len(bm25_scores)), key=lambda i: -bm25_scores[i])[:top_k]
    bm25_docs = [chunks[i] for i in bm25_top_idx]
    
    candidate = {id(d): d for d in vec_docs + bm25_docs}.values()
    reranked = await cross_rerank(query, list(candidate))
    return reranked[:top_n]