from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from .database import Base
from datetime import datetime

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    deadline = Column(DateTime)
    done = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    blacklisted_on = Column(DateTime, default=datetime.utcnow)
