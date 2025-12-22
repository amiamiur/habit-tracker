from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import users, habits, auth, habit_logs
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Habit Tracker API is running"}
app.include_router(users.router)
app.include_router(habits.router)
app.include_router(habit_logs.router)
app.include_router(auth.router)