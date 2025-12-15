import uvicorn
from fastapi import FastAPI

from app.database import engine
from app import models

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit Tracker API")

@app.get("/")
def read_root():
    return {"status": "ok"}

