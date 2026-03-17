from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, String
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """Read-only reference for FK — managed by Better Auth on the frontend."""

    __tablename__ = "user"

    id: str = Field(primary_key=True)
    email: str = Field(sa_column=Column("email", String, unique=True))
    name: str
    created_at: datetime | None = Field(
        default=None, sa_column=Column("createdAt", DateTime)
    )


class Task(SQLModel, table=True):
    __tablename__ = "task"

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
