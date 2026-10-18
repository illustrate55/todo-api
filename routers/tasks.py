"""HTTP API на FastAPI."""
from fastapi import APIRouter, Depends, HTTPException, status

from schemas import Task, TaskCreate, TaskUpdate, TaskDoneUpdate
from tasks import (
    task_get, 
    task_add, 
    task_update_by_position,
    task_set_done_by_position,
    task_delete_by_position
)
from users import get_current_user

router = APIRouter()


@router.get("/tasks", response_model=list[Task])
def list_tasks(current_user: dict = Depends(get_current_user)):
    return task_get(current_user["id"])


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, current_user: dict = Depends(get_current_user)):
    return task_add(current_user["id"], payload.title)


@router.put("/tasks/{task_id}", response_model=Task)
def update_task(position: int, payload: TaskUpdate, current_user: dict = Depends(get_current_user)):
    task = task_update_by_position(current_user["id"], position, payload.title)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/tasks/{position}/done", response_model=Task)
def set_task_done(position: int, payload: TaskDoneUpdate, current_user: dict = Depends(get_current_user)):
    task = task_set_done_by_position(current_user["id"], position, payload.done)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(position: int, current_user: dict = Depends(get_current_user)):
    if not task_delete_by_position(current_user["id"], position):
        raise HTTPException(status_code=404, detail="Task not found")