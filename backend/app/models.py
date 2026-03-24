from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, String
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """Read-only reference for FK — managed by Better Auth on the frontend."""

    __tablename__ = "user"

    id: str = Field(primary_key=True)
    email: str = Field(sa_column=Column("email", String, unique=True))
    name: str
    email_verified: bool = Field(
        default=False, sa_column=Column("emailVerified", Boolean)
    )
    image: str | None = Field(default=None)
    created_at: datetime | None = Field(
        default=None, sa_column=Column("createdAt", DateTime)
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column("updatedAt", DateTime)
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


class Conversation(SQLModel, table=True):
    __tablename__ = "conversation"

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class Message(SQLModel, table=True):
    __tablename__ = "message"

    id: int | None = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: str = Field(index=True)
    role: str
    content: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
