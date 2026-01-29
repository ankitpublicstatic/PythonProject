from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100),unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    agree_to_terms = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

