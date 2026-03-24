from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.auth import verify_user_access
from app.database import get_session
from app.models import Conversation, Message
from app.schemas import ChatRequest, ChatResponse

from agent.agent import run_agent

router = APIRouter(prefix="/api/{user_id}/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: str = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    # Get or create conversation
    if request.conversation_id:
        conversation = session.exec(
            select(Conversation).where(
                Conversation.id == request.conversation_id,
                Conversation.user_id == user_id,
            )
        ).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # Fetch conversation history
    history = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
    ).all()

    # Store user message
    user_message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content=request.message,
    )
    session.add(user_message)
    session.commit()

    # Build messages for agent
    messages = [{"role": m.role, "content": m.content} for m in history]
    messages.append({"role": "user", "content": request.message})

    # Run agent
    try:
        response_text, tool_calls = await run_agent(user_id, messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

    # Store assistant response
    assistant_message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="assistant",
        content=response_text,
    )
    session.add(assistant_message)

    # Update conversation timestamp
    conversation.updated_at = datetime.now(timezone.utc)
    session.add(conversation)
    session.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        response=response_text,
        tool_calls=tool_calls,
    )
