"""
FastAPI: Session, Cookie, Middleware, Security API Development, ORM.

FastAPI is a modern web framework for building APIs with Python 3.7+, based on Starlette and Pydantic.
It's async-friendly, auto-generates docs (Swagger/OpenAPI).

Sessions: Sessions store user data across requests. FastAPI doesn't have built-in sessions;
use starlette.middleware.sessions.SessionMiddleware to create new sessions. or third party like fastapi-users.

FastAPI: Sessions, Cookies, Middleware, Security API Development, ORM
FastAPI is a modern, fast (ASGI-based) web framework for APIs, auto-generating OpenAPI docs. Uses Pydantic for validation, Starlette for routing.

Sessions: Server-side storage (e.g., via Redis) for user state, as HTTP is stateless. Use fastapi_sessions or custom.
Cookies: Client-side storage via Response.set_cookie(). Secure with httponly=True, secure=True.
Middleware: Hooks into request/response cycle (e.g., CORS, logging). Added via app.add_middleware().
Security API Development: Uses OAuth2, JWT (via python-jose), dependencies for auth (Depends(OAuth2PasswordBearer)).
ORM: Integrates SQLAlchemy (or Tortoise) for DB models. Pydantic models for schemas.

Deep example: A simple user API with auth, sessions (simulated in-memory), cookies, middleware, SQLAlchemy ORM.
First, install note: Assume pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt].

"""
from copy import deepcopy
from datetime import time

# Example with middleware

from fastapi import FastAPI, Request, Response
from fastapi.security import APIKeyHeader

app = FastAPI()

@app.get("/")
async def root(request: Request):
    request.session['counter'] = request.session.get('counter',0)+1
    return {"counter": request.session['counter']}

# Cookies: Handle cookies via Response.set_cookie() and Request.cookies.

@app.get("/set-cookie")
async def set_cookie(request: Request, response: Response):
    response.set_cookie(key="my_cookie", value="hello", httponly=True, secure=True)
    return {"message": "Cookie set"}

@app.get("/get-cookie")
async def get_cookie(request: Request, response: Response):
    return {"cookie": request.cookies.get("my_cookie")}

# Middleware: Custom src that runs before/after requests. Add via app.add_middleware()
# Example: Session middleware

from starlette.middleware.sessions import SessionMiddleware

app.add_middleware(SessionMiddleware,secret_key="my-secret") # Enables sessions

# Now sessions work as above

# Custom middleware:

from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print (f"Request: {request.method} {request.url}")
        response = await call_next(request)
        return response

app.add_middleware(LoggingMiddleware)

# Security API Development:
# FastAPI supports OAuth2, JWT, API keys via fastapi.security. Use dependencies for auth.

# API key in header

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != "my-secret":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

@app.get("/secure", dependencies=[Depends(get_api_key)])
def secure_endpoint(request: Request, response: Response):
    return {"message": "Secure endpoint access successful"}

# For JWT/OAuth: Use OAuth2PasswordBearer for token-based auth.

"""
ORM: FastAPI integrates with ORM like SQLAlchemy for database ops. Pydantic for models
Example with SQLAlchemy ORM:
first install fastapi[all] sqlalchemy[all]

"""

from sqlalchemy import create_engine, Column, Integer, String
from  sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id  = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
def read_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return {"name": user.name, "email": user.email if user else "Not found"}

############################

from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

# Config
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
Base = declarative_base()

# ORM: SQLAlchemy Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

engine = create_engine("sqlite:///./test.db")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for DB session (ORM)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schemas
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fake sessions (in-memory dict; use Redis in prod)
sessions = {}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# Middleware: CORS and Logging
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request, call_next):
    print(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Response status: {response.status_code}")
    return response

# Routes
@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), response: Response = None, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    # Set cookie
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=False)  # secure=True in prod HTTPS
    # Simulate session
    sessions[user.username] = {"token": access_token, "login_time": datetime.utcnow()}
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check session
    if current_user.username not in sessions:
        raise HTTPException(status_code=401, detail="Session expired")
    return {"username": current_user.username, "session_active": True}

# Run with: uvicorn main:app --reload

"""

Explanation:

ORM: SQLAlchemy defines User model; get_db() injects sessions.
Security: JWT for tokens, bcrypt for passwords. /token endpoint handles login.
Cookies: Set via response.set_cookie() during login.
Sessions: In-memory dict (replace with Redis); checked in protected routes.
Middleware: CORS enables cross-origin; custom logs requests.
API Development: Auto-docs at /docs. Protected route uses Depends for auth.

Test: POST /users/ with {"username":"test","password":"test"}, then POST /token, GET /users/me with Bearer token.

"""
"""
Deepcopy & Shallow Copy
Copying objects: Shallow copy duplicates the objects but shares references to nested mutable objects. 
Deepcopy recursively copies everything from nested objects to nested mutable objects.

Use copy module

Deepcopy vs Shallow Copy
Both from copy module. Shallow copy (copy.copy() or list slicing) copies the top-level object but shares nested references (mutating nested affects both). Deep copy (copy.deepcopy()) recursively copies everything, fully independent.
Depth: Nested lists/dicts, cycles (deepcopy handles via memo).
"""

import copy

original =[1,[2,3]] # Nested list
shallow = copy.copy(original) # or original[:]

shallow[0] = 4 # Doesn't affect original
shallow[1][0] = 5 # Affects original's nested list

print(shallow)
print(original)

deep_copy = copy.deepcopy(original)
deep_copy[1][0] = 6 # Doesn't affect original
print(deep_copy)
print(original)

"""
Shallow is faster but risky for mutalbe nested structures. Deepcopy is safer for 
complex objects but slower and may not handle cycles well (Use copy.deepcopy with care.)
For custom classes, implement __copy__ and __deepcopy__ methods.
"""

import copy

# Original nested structure
original = [1, 2, [3, 4], {"key": [5]}]

# Shallow copy
shallow = copy.copy(original)
shallow[2][0] = 99  # Mutates nested in original too
shallow[3]["key"][0] = 999

print("Original after shallow mutate:", original)  # [1, 2, [99, 4], {'key': [999]}]

# Reset original
original = [1, 2, [3, 4], {"key": [5]}]

# Deep copy
deep = copy.deepcopy(original)
deep[2][0] = 888
deep[3]["key"][0] = 777

print("Original after deep mutate:", original)     # Unchanged: [1, 2, [3, 4], {'key': [5]}]
print("Deep copy:", deep)                         # [1, 2, [888, 4], {'key': [777]}]

# List slicing is shallow
sliced = original[:]
sliced.append(6)  # Doesn't affect original
print("Sliced append:", original)  # Unchanged

# Cycle example (deepcopy handles)
cyclic = [1, 2]
cyclic.append(cyclic)  # Self-reference
shallow_cyclic = copy.copy(cyclic)
# shallow_cyclic.append(3)  # Fine, but shared ref

deep_cyclic = copy.deepcopy(cyclic)  # Recursively copies, avoids infinite loop via memo
print("Cyclic deep works:", len(deep_cyclic))  # 3 (list + two elements, but ref is copied)

# Use shallow for flat structures, deep for nested to avoid surprises. Deepcopy is slower due to recursion.