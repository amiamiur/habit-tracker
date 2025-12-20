from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models
from app.schemas import HabitCreate, HabitResponse, HabitStatsResponse
from app.dependencies import get_db, get_current_user
from datetime import date, timedelta


router = APIRouter(
    prefix="/habits",
    tags=["Habits"]
)


@router.post("/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(
    habit: HabitCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_habit = models.Habit(
        title=habit.title,
        description=habit.description,
        is_active=habit.is_active,
        owner_id=current_user.id,
    )

    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)

    return db_habit


@router.get("/", response_model=list[HabitResponse])
def get_habits(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Habit)
        .filter(models.Habit.owner_id == current_user.id)
        .all()
    )

@router.get("/{habit_id}/stats", response_model=HabitStatsResponse)
def get_habit_stats(
    habit_id: int,
    db: Session = Depends(get_db),
):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    logs = (
        db.query(models.HabitLog)
        .filter(models.HabitLog.habit_id == habit_id)
        .order_by(models.HabitLog.date.asc())
        .all()
    )

    if not logs:
        return HabitStatsResponse(
            habit_id=habit_id,
            current_streak=0,
            max_streak=0,
            completion_rate=0.0,
        )

    completed_dates = [log.date for log in logs if log.completed]

    #completion rate
    completion_rate = len(completed_dates) / len(logs)

    #streaks (серия без пропусков)
    max_streak = 0
    current_streak = 0
    streak = 0
    prev_date = None

    for d in completed_dates:
        if prev_date and d == prev_date + timedelta(days=1):
            streak += 1
        else:
            streak = 1

        max_streak = max(max_streak, streak)
        prev_date = d

    # current streak — считаем с конца
    today = date.today()
    streak = 0
    prev_date = None

    for d in reversed(completed_dates):
        if prev_date is None:
            if d in (today, today - timedelta(days=1)):
                streak = 1
            else:
                break
        elif d == prev_date - timedelta(days=1):
            streak += 1
        else:
            break

        prev_date = d

    current_streak = streak

    return HabitStatsResponse(
        habit_id=habit_id,
        current_streak=current_streak,
        max_streak=max_streak,
        completion_rate=round(completion_rate * 100, 2),
    )