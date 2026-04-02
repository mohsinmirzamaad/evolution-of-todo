import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add backend dir to sys.path so 'app' package is importable when run as MCP subprocess
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server.fastmcp import FastMCP
from sqlmodel import Session, select

from app.database import engine
from app.models import Priority, Task

mcp_server = FastMCP("todo-mcp-server")


@mcp_server.tool()
def add_task(
    user_id: str,
    title: str,
    description: str = "",
    priority: str = "",
    due_date: str = "",
    tags: list[str] | None = None,
) -> str:
    """Add a new task for the user. Priority can be 'high', 'medium', or 'low'. Due date should be ISO format (e.g. '2026-05-01T00:00:00Z'). Tags is a list of strings."""
    with Session(engine) as session:
        parsed_priority = None
        if priority:
            try:
                parsed_priority = Priority(priority.lower())
            except ValueError:
                return json.dumps({"error": f"Invalid priority: {priority}. Use high, medium, or low."})

        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
            except ValueError:
                return json.dumps({"error": f"Invalid due_date format: {due_date}. Use ISO format."})

        task = Task(
            user_id=user_id,
            title=title,
            description=description or None,
            priority=parsed_priority,
            due_date=parsed_due_date,
            tags=tags or [],
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return json.dumps({
            "task_id": task.id,
            "status": "created",
            "title": task.title,
            "priority": task.priority.value if task.priority else None,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "tags": task.tags,
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
                "priority": t.priority.value if t.priority else None,
                "due_date": t.due_date.isoformat() if t.due_date else None,
                "tags": t.tags,
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
    user_id: str,
    task_id: int,
    title: str = "",
    description: str = "",
    priority: str = "",
    due_date: str = "",
    tags: list[str] | None = None,
) -> str:
    """Update a task's fields. Priority can be 'high', 'medium', or 'low'. Due date should be ISO format. Tags is a list of strings."""
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
        if priority:
            try:
                task.priority = Priority(priority.lower())
            except ValueError:
                return json.dumps({"error": f"Invalid priority: {priority}. Use high, medium, or low."})
        if due_date:
            try:
                task.due_date = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
            except ValueError:
                return json.dumps({"error": f"Invalid due_date format: {due_date}. Use ISO format."})
        if tags is not None:
            task.tags = tags
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        session.refresh(task)
        return json.dumps({
            "task_id": task.id,
            "status": "updated",
            "title": task.title,
            "priority": task.priority.value if task.priority else None,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "tags": task.tags,
        })
