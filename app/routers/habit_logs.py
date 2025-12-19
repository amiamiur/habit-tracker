from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models
from app.schemas import HabitLogCreate, HabitLogResponse
from app.dependencies import get_db

router = APIRouter(
    prefix="/habit-logs",
    tags=["Habit Logs"]
)


@router.post("/", response_model=HabitLogResponse, status_code=status.HTTP_201_CREATED)
def create_habit_log(
    log: HabitLogCreate,
    db: Session = Depends(get_db),
):
    habit = db.query(models.Habit).filter(models.Habit.id == log.habit_id).first()
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found"
        )

    habit_log = models.HabitLog(
        habit_id=log.habit_id,
        date=log.date,
        completed=log.completed
    )

    db.add(habit_log)
    db.commit()
    db.refresh(habit_log)

    return habit_log


@router.get("/", response_model=List[HabitLogResponse])
def get_habit_logs(
    db: Session = Depends(get_db),
):
    return db.query(models.HabitLog).all()
