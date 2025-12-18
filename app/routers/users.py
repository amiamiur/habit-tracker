from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app import models
from app.schemas import UserCreate, UserResponse
from app.dependencies import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    db_user = models.User(
        email=user.email,
        hashed_password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db),
):
    return db.query(models.User).all()

