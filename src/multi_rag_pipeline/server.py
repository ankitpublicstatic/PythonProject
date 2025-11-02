from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from rag_pipline import build_multi_rag, query_multi_rag

app = FastAPI(title="Multi-Source RAG Service")

# preload the retrievers at startup

vector_index, bm25, chunks = build_multi_rag()

class QueryRequest(BaseModel):
    query: str

@app.post("/rag/query")
async def rag_query(request: QueryRequest):
    answer = await asyncio.to_thread(query_multi_rag, request.query, vector_index, bm25, chunks)
    return {"query":request.query, "answer":answer}


"""
Run it
uvicorn server:app --reload --port 8000

curl -X POST http://localhost:8000/rag/query \
     -H "Content-Type: application/json" \
     -d '{"query": "Explain microservices communication patterns"}'

"""
#