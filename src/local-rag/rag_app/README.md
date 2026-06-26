rag_app/
│
├── app.py                # FastAPI
├── database.py           # DB connection
├── models.py             # SQLAlchemy models
├── chat_repository.py    # DB operations
├── rag_engine.py         # RAG logic
└── requirements.txt

rag_app/
│
├── app.py                # FastAPI server
├── ingest.py             # Multi-file ingestion
├── rag_engine.py         # Hybrid + Rerank + Memory + Streaming
├── chroma_db/
└── data/

                 ┌──────────────┐
                 │   FastAPI    │
                 │  (WebSocket) │
                 └──────┬───────┘
                        │
            ┌───────────▼────────────┐
            │        RAG Engine       │
            │ Hybrid + Rerank + Cache │
            └──────┬─────────┬───────┘
                   │         │
         ┌─────────▼─┐   ┌───▼────────┐
         │   Redis    │   │   Chroma   │
         │  (Cache)   │   │  VectorDB  │
         └────────────┘   └────────────┘
                   │
         ┌─────────▼─────────┐
         │ PostgreSQL (Chat) │
         └─────────┬─────────┘
                   │
         ┌─────────▼──────────┐
         │  OpenTelemetry     │
         └────────────────────┘