from __future__ import annotations

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import asyncio, os, redis
from rag_pipline import build_multi_rag, query_multi_rag

# Config
SECRET_KEY = "superankitsecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Mock user DB
fake_users_db = {
    "admin":{
        "username":"admin",
        "hashed_password":pwd_context.hash("User@123"),
    }
}

# Redis Cache
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_ = redis.Redis(host=redis_host, port=redis_port, db=0)

app = FastAPI(title="Multi-Source RAG Service with Auth & Cache")

# Preload RAG Resources

vector_index, bm25, chunks = build_multi_rag()

# Authentication

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp", expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"]},
                                       expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username

# RAG Query Endpoint
class QueryRequest(BaseModel):
    query: str

@app.post("/rag/query")
async def rag_query(request: QueryRequest, current_user: str = Depends(get_current_user)):
    cache_key = f"rag:{request.query}"
    cached = redis_.get(cache_key)
    if cached:
        return {"query": request.query, "answer": cached.decode(), "cached":True}

    answer = await asyncio.to_thread(query_multi_rag, request.query, vector_index, bm25, chunks)
    redis_.setex(cache_key, timedelta(hours=1), answer)
    return {"query": request.query, "answer": answer, "cached":False}



"""
🧠 Usage

Start Redis

$ redis-server


Run API

$ uvicorn server:app --reload --port 8000


Authenticate

curl -X POST -d "username=admin&password=User@123" http://localhost:8000/token


→ Returns access_token

Query with token

curl -X POST http://localhost:8000/rag/query \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"query":"Explain microservices communication patterns"}'


The first call stores the answer in Redis; subsequent identical queries are served instantly from cache.
"""

"""

Run everything

In the project root:

docker-compose up --build

| Service      | URL                                                      | Description                 |
| ------------ | -------------------------------------------------------- | --------------------------- |
| FastAPI API  | [http://localhost:8000/docs](http://localhost:8000/docs) | Test secured endpoints      |
| Streamlit UI | [http://localhost:8501](http://localhost:8501)           | Use your RAG assistant      |
| Redis        | Port 6379                                                | Used internally for caching |


| Component | Container   | Port | Purpose                         |
| --------- | ----------- | ---- | ------------------------------- |
| FastAPI   | `rag_api`   | 8000 | Backend API with auth & caching |
| Redis     | `rag_redis` | 6379 | Cache layer                     |
| Streamlit | `rag_ui`    | 8501 | Web UI frontend                 |

"""

"""
| Secret                  | Example value                                |
| ----------------------- | -------------------------------------------- |
| `AWS_ACCESS_KEY_ID`     | your AWS key                                 |
| `AWS_SECRET_ACCESS_KEY` | your AWS secret                              |
| `AWS_REGION`            | us-east-1                                    |
| `ECR_REPOSITORY`        | your-ecr-repository-name                     |
| `ECR_REGISTRY`          | <account-id>.dkr.ecr.us-east-1.amazonaws.com |
| `DOCKERHUB_USERNAME`    | (optional if using DockerHub)                |
| `DOCKERHUB_TOKEN`       | (optional if using DockerHub)                |

"""