from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: str
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime


class MessageResponse(BaseModel):
    message: str


class ChatRequest(BaseModel):
    conversation_id: int | None = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: list[dict] = []
