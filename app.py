"""HTTP API на FastAPI."""
from fastapi import FastAPI
from routers import auth, tasks

app = FastAPI(title="Todo API", version="1.0")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])