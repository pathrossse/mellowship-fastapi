from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Todo(BaseModel):
    description: str
    deadline: datetime
    done: bool

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True 
class Token(BaseModel):
    access_token: str
    refresh_token: str  
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    token_type: Optional[str] = None  
