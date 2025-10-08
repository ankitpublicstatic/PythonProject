"""
Security API Development (OAuth2 with JWT):
The Flow: 1. Login: The user sends their username and password to generate a /token endpoint.
2. Token Creation: The server verifies the credentials. if they are correct, it creates a JWT.
(A Signed, encoded string containing user information like user ID and an expiration date time)
3. Token Return: The Server returns this JWT to the client.
4. Protected Requests: For subsequent requests to protected endpoints, the client must include the
JWT in the Authorization header. usually as Bearer <token>.
5. Token Verification: The protected endpoint uses a dependency to verify the JWT's signature and expiration. if valid, it grant access.

FastAPI provides excellent tools in its fastapi.security module to streamline this.

Programming Example:

This is a simplified but functional example of a login endpoint and a protected endpoint.
"""

# Requires 'python-jose' and 'passlib' libraries: pip install "python-jose[cryptography]" "passlib[bcrypt]"
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


# ----  Configuration ----
SECRET_KEY = "oiw892390ksl" # In production, use a secure, random generated key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MINUTES = 30

# --- Setup ---
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token" ) # Points to the /token endpoint

# --- Helper Functions ---

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

# --- Dependency to get current user ---
async  def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # In a real app, you would fetch the user from the database here
    return { "username": username }

# --- API Endpoints ---
@app.post(
    "/token" )
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # In a real app, you would verify form_data.username and form_data.password against your database
    if form_data.username != "user" or form_data.password != "User@123":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    access_token = create_access_token(data={"sub":form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    # The get_current_user dependency runs first. If the token is invalid
    # this function will never be reached
    return current_user

"""
ORM: Object Relational Mapper or ODM: Object Document Mapper is a library that lets you query and manipulate data from 
a database using object-oriented paradigm. Instead of writing raw SQL or database queries, you interact with Python objects. 

PostgreSQL with SQLAlchemy ORM: 
SQLAlchemy is the de facto ORM for Python. It maps Python classes to tables in a relational database like PostgreSQL.
Steps:
1. Define a Python class that inherits from a declarative base. This class represents a database table. 
2. Create an "engine" that connects to your database.
3. Create "sessions" to handle transactions. You perform all your database operations within a session. 

Programming Example: This example defines a User model and creates endpoints to creating and reading users.  
"""

# Requires: pip install fastapi uvicorn sqlalchemy psycopg2-binary
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# --- Database Setup (SQLAlchemy) ---
DATABASE_URL = "postgresql://postgres:root@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- ORM Model ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

# Create the table in the database run this once
Base.metadata.create_all(bind=engine)

# --- Pydantic Model (for request/response) ---
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True # Allow Pydantic to read data from ORM objects

# --- Dependency to get DB session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

"""
MongoDB with Beanie (ODM: Object Document Mapper)
MongoDB is a NoSQL Document database. Instead of tables and rows, it stores data in JSON-like documents. 
Beanie is modern asynchronous ODM for MongoDB build on top of Pydantic and Motor. 

Programming Example: This example defines an Event document and creates async endpoints for managing it. 
"""

# Requires: pip install fastapi uvicorn beanie
import motor.motor_asyncio
from beanie import Document, init_beanie
from fastapi import FastAPI
from typing import List

# --- Beanie Document Model (maps to a MongoDB collection) ---
class Event(Document):
    name: str
    description: str
    class Settings:
        name = "events" # The MongoDB collection name

app = FastAPI()

# This is an async function that runs when the app starts

@app.on_event("startup")
async def on_startup():
    # --- Database Setup (Beanie) ----
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.events_db, document_models=[Event])

@app.post("/events", response_model=Event)
async def create_event(event: Event):
    await event.create()
    return event

@app.get("/events", response_model=List[Event])
async def read_events(events: List[Event]):
    events = await Event.find_all().to_list()
    return events

"""
Shallow copy: A shallow copy creates a new object, but instead of copying the nested objects within the
original, it simply copies references to them.
Implication: if you modify a nested object in the shallow copy, the change will be reflected in the original
object because both copies point to the exact same nested object.
It is created using copy.copy()

Deep Copy: A deep copy creates a new object and then, recursively, copies all the nested objects found in 
the original.
Implication: The copy is completely independent of the original. Modifying a nested object in the deep copy will 
not affect the original object. 
It is created using copy.deepcopy()
"""