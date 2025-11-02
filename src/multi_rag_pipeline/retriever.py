from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from rank_bm25 import BM25Okapi
from sympy.codegen.fnodes import dimension

from config import INDEX_NAME
from reranker import cross_rerank
import pinecone

def build_vector_index(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    if INDEX_NAME not in pinecone.list_indexes():
        pinecone.create_index(INDEX_NAME, dimension=1536)
    index = Pinecone.from_documents(chunks, embeddings, index_name=INDEX_NAME)
    return index, chunks

def build_bm25_index(chunks):
    tokenized = [c.page_content.split() for c in chunks]
    bm25 = BM25Okapi(tokenized)
    return bm25

def retrieve(query, vector_index, bm25, chunks, top_k=20):
    vec_docs = vector_index.similarity_search(query, k=top_k)
    bm25_scores = bm25.get_scores(query.split())
    bm25_top_idx = sorted(range(len(bm25_scores)), key=lambda i: -bm25_scores[i])[:top_k]
    bm25_docs = [chunks[i] for i in bm25_top_idx]

    # Merge + dedup
    unique = {d.page_content[:100]: d for d in vec_docs + bm25_docs}.values()
    return list(unique)

