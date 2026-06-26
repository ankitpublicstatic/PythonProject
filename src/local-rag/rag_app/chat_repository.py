from sqlalchemy.orm import Session
from models import User, ChatMessage

def get_or_create_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def save_message(db: Session, user_id: int, role: str, content: str):
    message = ChatMessage(user_id=user_id, role=role, content=content)
    db.add(message)
    db.commit()

def get_chat_history(db: Session, user_id: int, limit: int = 10):
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
        .all()
    )