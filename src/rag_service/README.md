
## Folder Structure

- rag_service/
- │
- ├── app.py                   # FastAPI app (REST service)
- ├── retrievers.py            # Vector + BM25 retrieval logic
- ├── reranker.py              # Cross-encoder reranking
- ├── chain.py                 # LangChain orchestration
- ├── requirements.txt
- └── data/
- -    ├── docs/                # Raw documents
- -    └── embeddings/          # Vector DB files
