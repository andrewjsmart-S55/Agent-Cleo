"""
Chat API Routes - Agent conversation endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from ..database import get_db, AgentDB, ChatSessionDB, AgentStatusEnum
from ..models import ChatRequest, ChatResponse
from ..overlord_client.client import get_overlord_client

router = APIRouter(prefix="/chat")


@router.post("", response_model=ChatResponse)
async def chat_with_agent(
    chat_request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Chat with a specific agent"""
    # Get agent
    agent = db.query(AgentDB).filter(AgentDB.id == chat_request.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # Get or create session
    session_id = chat_request.session_id or str(uuid.uuid4())
    session = db.query(ChatSessionDB).filter(ChatSessionDB.id == session_id).first()

    if not session:
        session = ChatSessionDB(
            id=session_id,
            agent_id=chat_request.agent_id,
            messages=[]
        )
        db.add(session)

    # Build system prompt for agent
    system_prompt = f"""You are {agent.name}, an AI agent specialized in {agent.tier.value} tier operations.

Your capabilities: {', '.join(agent.capabilities or [])}

{agent.description or 'You help users with various tasks based on your expertise.'}

Always stay in character and use your specialized knowledge to provide helpful, accurate responses."""

    # Get conversation context
    messages = session.messages or []
    context = [{"role": msg["role"], "content": msg["content"]} for msg in messages[-10:]]

    # RAG context placeholder
    rag_context = []
    if chat_request.use_rag:
        # RAG query implementation would go here
        pass

    # Get AI response from Overlord
    overlord_client = await get_overlord_client()
    ai_response = await overlord_client.chat_completion(
        message=chat_request.message,
        system_prompt=system_prompt,
        agent_name=agent.name,
        context=context
    )

    if not ai_response.get("success"):
        raise HTTPException(status_code=500, detail="Failed to get AI response")

    # Update session
    messages.append({
        "role": "user",
        "content": chat_request.message,
        "timestamp": datetime.utcnow().isoformat()
    })
    messages.append({
        "role": "assistant",
        "content": ai_response["message"],
        "timestamp": datetime.utcnow().isoformat()
    })
    session.messages = messages
    session.updated_at = datetime.utcnow()

    # Update agent last active
    agent.last_active = datetime.utcnow()
    agent.status = AgentStatusEnum.IDLE

    db.commit()

    return ChatResponse(
        session_id=session_id,
        agent_id=agent.id,
        agent_name=agent.name,
        message=ai_response["message"],
        sources=rag_context if chat_request.use_rag else None,
        timestamp=datetime.utcnow()
    )
