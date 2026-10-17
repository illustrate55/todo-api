"""Pydantic-модели для HTTP-слоя."""
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=500)


class TaskDoneUpdate(BaseModel):
    done: bool


class Task(BaseModel):
    id: int
    position: int
    title: str
    done: bool