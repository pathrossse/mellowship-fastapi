from sqlmodel import SQLModel, Field, Column, DataTime, Relationship
from typing import Optional, List
from datetime import datetime
from pydantic import EmailStr

class Todo(SQLModel, table=true):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = Field(index=True)
    deadline: Optional[datetime] = Field(sa_column=Column(DateTime))
    done: bool = Field(default=False)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")

class User(SQLModel, table=true):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    password: str

class BlacklistedToken(SQLModel, table=true):
    __tablename__ = "blacklisted_tokens"    

    id: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(unique=True, index=True)
    blacklisted_on: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))
