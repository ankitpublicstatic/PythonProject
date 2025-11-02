import time, numpy as np
from retrievers import splitter, chunks, faiss_index, bm25
from reranker import cross_rerank

def benchmark_chunk_sizes(query: str, chunk_sizes=[256, 512, 768]):
    results = []
    for size in chunk_sizes:
        splitter.chunk_size = size
        start = time.time()
        docs = faiss_index.similarity_search(query, k=20)
        reranked = cross_rerank(query, docs)
        duration = time.time() - start
        results.append((size,duration, reranked[0].page_content[:100]))
    return results

def benchmark_rerank_thresholds(query:str, top_k_values=[10,30,50]):
    time, quality = [], []
    for k in top_k_values:
        start = time.time()
        docs = faiss_index.similarity_search(query, k=k)
        reranked = cross_rerank(query, docs)
        duration = time.time() - start
        time.append(duration)
        quality.append(reranked[0].page_content[:100])
    return list(zip(top_k_values, time, quality))

if __name__ == "__main__":
    query = "Explain circuit breaker design pattern"
    print("Chunk Benchmark: ",benchmark_chunk_sizes(query))
    print("Rerank Thresholds: ",benchmark_rerank_thresholds(query))

