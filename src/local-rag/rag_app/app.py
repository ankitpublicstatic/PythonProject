from tracing import tracer
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket, Depends
from rag_engine import generate_answer, stream_answer_on_console, stream_answer, generate_answer_quick

from sqlalchemy.orm import Session
from database import SessionLocal
from chat_repository import (
    get_or_create_user,
    save_message,
    get_chat_history,
)

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/stream_console")
async def ask_question(req: QueryRequest):
    with tracer.start_as_current_span("rag_query"):
        stream_answer_on_console(req.question)
    return {"status": "Answer streamed in console"}

@app.post("/ask")
async def ask_question(req: QueryRequest):
    with tracer.start_as_current_span("rag_query"):
        result = generate_answer(req.question)
    return result

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        query = await websocket.receive_text()

        async for token in stream_answer(query):
            await websocket.send_text(token)




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChatRequest(BaseModel):
    username: str
    question: str

@app.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):

    # Get user
    user = get_or_create_user(db, req.username)

    # Fetch history
    history = get_chat_history(db, user.id, limit=10)

    # Generate answer
    answer = generate_answer_quick(req.question, history)

    # Save user message
    save_message(db, user.id, "user", req.question)

    # Save assistant response
    save_message(db, user.id, "assistant", answer)

    return {"answer": answer}


# uvicorn app:app --reload
# POST http://127.0.0.1:8000/chat
# {
#   "username": "ankit",
#   "question": "What is RAG?"
# }