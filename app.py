"""HTTP API на FastAPI."""
from fastapi import FastAPI, HTTPException, status

from db import init_db
from schemas import Task, TaskCreate, TaskUpdate
from tasks import task_get, task_add, task_update_by_position, task_delete_by_position

app = FastAPI(title="Todo API", version="1.0")
init_db()


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return task_get()


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    return task_add(payload.title)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(position: int, payload: TaskUpdate):
    task = task_update_by_position(position, payload.title)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(position: int):
    if not task_delete_by_position(position):
        raise HTTPException(status_code=404, detail="Task not found")