from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, col, select

from app.auth import verify_user_access
from app.database import get_session
from app.models import Priority, Task
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


@router.get("/search", response_model=list[TaskResponse])
def search_tasks(
    user_id: str = Depends(verify_user_access),
    q: str | None = Query(default=None, description="Search keyword in title/description"),
    status_filter: str = Query(default="all", description="all, pending, or completed"),
    priority: Priority | None = Query(default=None, description="Filter by priority"),
    tag: str | None = Query(default=None, description="Filter by tag"),
    due_before: datetime | None = Query(default=None, description="Tasks due before this date"),
    due_after: datetime | None = Query(default=None, description="Tasks due after this date"),
    sort_by: str = Query(default="created_at", description="created_at, due_date, priority, title"),
    sort_order: str = Query(default="desc", description="asc or desc"),
    session: Session = Depends(get_session),
):
    query = select(Task).where(Task.user_id == user_id)

    if q:
        query = query.where(
            col(Task.title).icontains(q) | col(Task.description).icontains(q)
        )
    if status_filter == "pending":
        query = query.where(Task.completed == False)  # noqa: E712
    elif status_filter == "completed":
        query = query.where(Task.completed == True)  # noqa: E712
    if priority:
        query = query.where(Task.priority == priority)
    if tag:
        query = query.where(col(Task.tags).contains([tag]))
    if due_before:
        query = query.where(col(Task.due_date) <= due_before)
    if due_after:
        query = query.where(col(Task.due_date) >= due_after)

    sort_columns = {
        "created_at": Task.created_at,
        "due_date": Task.due_date,
        "priority": Task.priority,
        "title": Task.title,
    }
    sort_col = sort_columns.get(sort_by, Task.created_at)
    if sort_order == "asc":
        query = query.order_by(col(sort_col).asc())
    else:
        query = query.order_by(col(sort_col).desc())

    return session.exec(query).all()


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
