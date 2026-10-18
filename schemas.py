"""Pydantic-модели для HTTP-слоя."""
from pydantic import BaseModel, Field

# --- Задачи ---
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

# --- Пользователи ---
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)

class UserRead(BaseModel):
    id: int
    username: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str