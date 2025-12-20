from app.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Generator
from fastapi import Depends, HTTPException
from app.database import SessionLocal
from app import models


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db)) -> models.User:
    user = db.query(models.User).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user