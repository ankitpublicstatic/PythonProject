from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "rag_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

    messages = relationship(
        "ChatMessage",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("rag_users.id"))

    role = Column(String)  # user / assistant
    content = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="messages")