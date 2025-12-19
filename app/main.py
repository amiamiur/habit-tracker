import uvicorn
from fastapi import FastAPI

from app.database import engine
from app import models
from app.routers import users, habits
from app.routers import habit_logs
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Habit Tracker API",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "Habit Tracker API is running"}


app.include_router(users.router)
app.include_router(habits.router)
app.include_router(habit_logs.router)

@app.on_event("startup")
def on_startup():
    # Создаём таблицы при старте (только для разработки)
    models.Base.metadata.create_all(bind=engine)