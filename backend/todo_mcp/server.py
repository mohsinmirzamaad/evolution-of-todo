import json
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP
from sqlmodel import Session, select

from app.database import engine
from app.models import Task

mcp_server = FastMCP("todo-mcp-server")


@mcp_server.tool()
def add_task(user_id: str, title: str, description: str = "") -> str:
    """Add a new task for the user. Returns the created task info."""
    with Session(engine) as session:
        task = Task(
            user_id=user_id,
            title=title,
            description=description or None,
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return json.dumps({
            "task_id": task.id,
            "status": "created",
            "title": task.title,
        })


@mcp_server.tool()
def list_tasks(user_id: str, status: str = "all") -> str:
    """List tasks for the user. Status can be 'all', 'pending', or 'completed'."""
    with Session(engine) as session:
        query = select(Task).where(Task.user_id == user_id)
        if status == "pending":
            query = query.where(Task.completed == False)  # noqa: E712
        elif status == "completed":
            query = query.where(Task.completed == True)  # noqa: E712
        tasks = session.exec(query).all()
        return json.dumps([
            {
                "task_id": t.id,
                "title": t.title,
                "description": t.description,
                "completed": t.completed,
            }
            for t in tasks
        ])


@mcp_server.tool()
def complete_task(user_id: str, task_id: int) -> str:
    """Mark a task as completed. Returns the updated task info."""
    with Session(engine) as session:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()
        if not task:
            return json.dumps({"error": f"Task {task_id} not found"})
        task.completed = True
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        session.refresh(task)
        return json.dumps({
            "task_id": task.id,
            "status": "completed",
            "title": task.title,
        })


@mcp_server.tool()
def delete_task(user_id: str, task_id: int) -> str:
    """Delete a task. Returns the deleted task info."""
    with Session(engine) as session:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()
        if not task:
            return json.dumps({"error": f"Task {task_id} not found"})
        title = task.title
        session.delete(task)
        session.commit()
        return json.dumps({
            "task_id": task_id,
            "status": "deleted",
            "title": title,
        })


@mcp_server.tool()
def update_task(
    user_id: str, task_id: int, title: str = "", description: str = ""
) -> str:
    """Update a task's title or description. Returns the updated task info."""
    with Session(engine) as session:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()
        if not task:
            return json.dumps({"error": f"Task {task_id} not found"})
        if title:
            task.title = title
        if description:
            task.description = description
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        session.refresh(task)
        return json.dumps({
            "task_id": task.id,
            "status": "updated",
            "title": task.title,
        })
