from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class HabitBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_active: bool = True

class HabitCreate(HabitBase):
    pass

class HabitUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class HabitResponse(HabitBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class HabitLogCreate(BaseModel):
    date: date

class HabitLogResponse(BaseModel):
    id: int
    date: date
    habit_id: int

    class Config:
        from_attributes = True
