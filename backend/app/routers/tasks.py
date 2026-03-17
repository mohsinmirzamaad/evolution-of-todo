from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.auth import verify_user_access
from app.database import get_session
from app.models import Task
from app.schemas import MessageResponse, TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    user_id: str = Depends(verify_user_access),
    status_filter: str = "all",
    session: Session = Depends(get_session),
):
    query = select(Task).where(Task.user_id == user_id)
    if status_filter == "pending":
        query = query.where(Task.completed == False)  # noqa: E712
    elif status_filter == "completed":
        query = query.where(Task.completed == True)  # noqa: E712
    return session.exec(query).all()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    task = Task(user_id=user_id, **task_data.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/{id}", response_model=TaskResponse)
def get_task(
    id: int,
    user_id: str = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    task = session.exec(
        select(Task).where(Task.id == id, Task.user_id == user_id)
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{id}", response_model=TaskResponse)
def update_task(
    id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    task = session.exec(
        select(Task).where(Task.id == id, Task.user_id == user_id)
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{id}", response_model=MessageResponse)
def delete_task(
    id: int,
    user_id: str = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    task = session.exec(
        select(Task).where(Task.id == id, Task.user_id == user_id)
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return MessageResponse(message="Task deleted")


@router.patch("/{id}/complete", response_model=TaskResponse)
def toggle_complete(
    id: int,
    user_id: str = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    task = session.exec(
        select(Task).where(Task.id == id, Task.user_id == user_id)
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = not task.completed
    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
