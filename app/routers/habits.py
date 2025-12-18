from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app import models
from app.schemas import HabitCreate, HabitResponse
from app.dependencies import get_db

router = APIRouter(
    prefix="/habits",
    tags=["Habits"]
)

fake_habits_db = []


@router.post("/", response_model=HabitResponse)
def create_habit(
    habit: HabitCreate,
    owner_id: int,
    db: Session = Depends(get_db),
):
    db_habit = models.Habit(
        title=habit.title,
        description=habit.description,
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

