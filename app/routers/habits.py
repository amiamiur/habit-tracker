from fastapi import APIRouter
from typing import List

from app.schemas import HabitCreate, HabitUpdate, HabitResponse

router = APIRouter(
    prefix="/habits",
    tags=["Habits"]
)

fake_habits_db = []


@router.post("/", response_model=HabitResponse)
def create_habit(habit: HabitCreate):
    new_habit = {
        "id": len(fake_habits_db) + 1,
        "title": habit.title,
        "description": habit.description
    }
    fake_habits_db.append(new_habit)
    return new_habit


@router.get("/", response_model=List[HabitResponse])
def get_habits():
    return fake_habits_db
