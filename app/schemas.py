from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class HabitCreate(BaseModel):
    title: str
    description: Optional[str] = None

class HabitUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class HabitResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]

    class Config:
        from_attributes = True
