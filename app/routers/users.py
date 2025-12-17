from fastapi import APIRouter
from typing import List

from app.schemas import UserCreate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# ВРЕМЕННОЕ хранилище
fake_users_db = []


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    new_user = {
        "id": len(fake_users_db) + 1,
        "email": user.email
    }
    fake_users_db.append(new_user)
    return new_user


@router.get("/", response_model=List[UserResponse])
def get_users():
    return fake_users_db
