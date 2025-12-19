from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Date
from datetime import date

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    habits = relationship("Habit", back_populates="owner", cascade="all, delete")


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="habits")

    logs = relationship(
        "HabitLog",
        back_populates="habit",
        cascade="all, delete"
    )

class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)

    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    habit = relationship("Habit", back_populates="logs")