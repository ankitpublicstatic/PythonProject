from fastapi import FastAPI
from pydantic import BaseModel
from chain import get_answer

app = FastAPI(title="Multi-RAG LangChain Service")

class QueryRequest(BaseModel):
    query:str

@app.post("/rag/query")
async def rag_query(request: QueryRequest):
    answer = await get_answer(request.query)
    return {"query": request.query, "answer":answer}