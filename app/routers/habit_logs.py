import datetime
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

@router.post("/{habit_id}/logs", response_model=HabitLogResponse)
def create_habit_log(
    habit_id: int,
    log: HabitLogCreate,
    db: Session = Depends(get_db),
):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    db_log = models.HabitLog(
        habit_id=habit_id,
        date=log.date or datetime.date.today(),
        completed=log.completed
    )

    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    return db_log


@router.get("/", response_model=List[HabitLogResponse])
def get_habit_logs(
    db: Session = Depends(get_db),
):
    return db.query(models.HabitLog).all()

@router.get("/{habit_id}/logs", response_model=list[HabitLogResponse])
def get_habit_logs(
    habit_id: int,
    db: Session = Depends(get_db),
):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    return (
        db.query(models.HabitLog)
        .filter(models.HabitLog.habit_id == habit_id)
        .order_by(models.HabitLog.date.desc())
        .all()
    )

