from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models
from app.schemas import HabitCreate, HabitResponse
from app.dependencies import get_db

router = APIRouter(
    prefix="/habits",
    tags=["Habits"]
)


@router.post("/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(
    habit: HabitCreate,
    owner_id: int,
    db: Session = Depends(get_db),
):
    # Проверяем, существует ли пользователь
    user = db.query(models.User).filter(models.User.id == owner_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db_habit = models.Habit(
        title=habit.title,
        description=habit.description,
        is_active=habit.is_active,
        owner_id=owner_id
    )

    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)

    return db_habit


@router.get("/", response_model=List[HabitResponse])
def get_habits(
    db: Session = Depends(get_db),
):
    return db.query(models.Habit).all()