import uvicorn
from fastapi import FastAPI

from app.database import engine
from app import models
from app.routers import users, habits

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

