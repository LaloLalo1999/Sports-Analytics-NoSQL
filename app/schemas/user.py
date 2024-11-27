from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class NotificationBase(BaseModel):
    message: str
    date: datetime
    read: bool = False

class UserResponse(UserBase):
    id: str
    favorite_teams: List[str] = []
    favorite_players: List[str] = []
    notifications: List[NotificationBase] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer" 