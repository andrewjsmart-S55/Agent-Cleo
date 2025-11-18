"""
Agent-Cleo v2.0 - Professional UX with Studio55IQ Integration
FastAPI backend combining multi-agent orchestration with RAG capabilities
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Optional
from pathlib import Path
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import os
import json
import uuid

from src.config import settings
from src.database import get_db, init_db, AgentDB, JobDB, ActivityDB, ChatSessionDB, AgentTierEnum, AgentStatusEnum
from src.models import (
    Agent, AgentCreate, AgentUpdate,
    Job, JobCreate, JobUpdate,
    Activity, ActivityCreate,
    ChatRequest, ChatResponse, ChatMessage,
    QueryRequest, QueryResponse,
    TodoistTaskCreate, TodoistTaskResponse,
    HealthCheck,
    AgentGraph, AgentNode, AgentEdge,
    AgentHierarchy
)
from src.overlord_client.client import get_overlord_client

# Optional Todoist integration
try:
    from todoist_integration import TodoistIntegration, create_task_for_andrew
    TODOIST_ENABLED = True
except ImportError:
    print("Warning: Todoist integration not available")
    TODOIST_ENABLED = False
    TodoistIntegration = None
    create_task_for_andrew = None


# ============================================================================
# APPLICATION LIFECYCLE
# ============================================================================

# Global cache for discovered agents
_agents_cache = None
_agents_cache_timestamp = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    global _agents_cache, _agents_cache_timestamp

    # Startup
    print("=" * 70)
    print("Agent-Cleo v2.0 - Professional AI Agent Orchestration")
    print("=" * 70)
    print(f"Initializing database...")
    init_db()
    print(f"Database initialized: {settings.database_url}")
    print(f"Overlord API: {settings.overlord_api_url}")
    print(f"Base Path: {settings.base_path}")

    # Initialize empty cache (agent folders not in Docker container)
    # In production, agents are managed via database, not filesystem
    _agents_cache = []
    _agents_cache_timestamp = datetime.utcnow()
    print(f"Agent cache initialized (empty - agents managed via database)")

    print("=" * 70)

    yield

    # Shutdown
    print("Shutting down Agent-Cleo...")


# ============================================================================
# INITIALIZE FASTAPI APP
# ============================================================================

app = FastAPI(
    title="Agent-Cleo",
    version="2.0.0",
    description="Professional AI Agent Orchestration with RAG",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ============================================================================
# MAIN ROUTES
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main application interface"""
    return templates.TemplateResponse("index_new.html", {"request": request})


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """System health check"""
    overlord_client = await get_overlord_client()
    overlord_healthy = await overlord_client.health_check()

    return HealthCheck(
        status="healthy",
        version=settings.app_version,
        database=True,  # If we got here, DB is working
        rag_engine=True,  # TODO: Implement RAG health check
        overlord=overlord_healthy
    )


# ============================================================================
# AGENT ROUTES
# ============================================================================

@app.get("/api/agents", response_model=List[Agent])
async def get_agents(
    tier: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all agents with optional filtering"""
    query = db.query(AgentDB)

    if tier:
        query = query.filter(AgentDB.tier == tier)
    if status:
        query = query.filter(AgentDB.status == status)

    agents = query.order_by(AgentDB.tier, AgentDB.name).all()
    return [Agent.model_validate(agent) for agent in agents]


@app.get("/api/agents/{agent_id}", response_model=Agent)
async def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """Get specific agent"""
    agent = db.query(AgentDB).filter(AgentDB.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return Agent.model_validate(agent)


@app.post("/api/agents", response_model=Agent)
async def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    """Create new agent"""
    db_agent = AgentDB(**agent.dict())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return Agent.model_validate(db_agent)


@app.put("/api/agents/{agent_id}", response_model=Agent)
async def update_agent(
    agent_id: int,
    agent_update: AgentUpdate,
    db: Session = Depends(get_db)
):
    """Update agent"""
    db_agent = db.query(AgentDB).filter(AgentDB.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    for key, value in agent_update.dict(exclude_unset=True).items():
        setattr(db_agent, key, value)

    db_agent.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_agent)
    return Agent.model_validate(db_agent)


@app.post("/api/agents/initialize")
async def initialize_agents(db: Session = Depends(get_db)):
    """Initialize all agents from cached discovery (fast - uses startup cache)"""
    global _agents_cache, _agents_cache_timestamp

    try:
        # Use cached agents data from startup
        if _agents_cache is None:
            raise HTTPException(
                status_code=503,
                detail="Agent cache not initialized. Server may still be starting up."
            )

        agents_data = _agents_cache
        created_count = 0
        updated_count = 0

        for agent_data in agents_data:
            existing = db.query(AgentDB).filter(
                AgentDB.folder_name == agent_data['folder_name']
            ).first()

            if existing:
                existing.name = agent_data['name']
                existing.path = agent_data['path']
                existing.context_summary = agent_data['context_summary']
                existing.tier = agent_data['tier']
                existing.updated_at = datetime.utcnow()
                updated_count += 1
            else:
                new_agent = AgentDB(
                    name=agent_data['name'],
                    folder_name=agent_data['folder_name'],
                    path=agent_data['path'],
                    tier=agent_data['tier'],
                    context_summary=agent_data['context_summary'],
                    capabilities=agent_data.get('capabilities', []),
                    status=AgentStatusEnum.IDLE
                )
                db.add(new_agent)
                created_count += 1

        db.commit()

        return {
            "success": True,
            "message": f"Initialized {len(agents_data)} agents",
            "created": created_count,
            "updated": updated_count,
            "cache_age": str(datetime.utcnow() - _agents_cache_timestamp) if _agents_cache_timestamp else "unknown"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/agents/refresh-cache")
async def refresh_agent_cache():
    """
    Admin endpoint: Refresh the agent discovery cache by re-scanning the filesystem.
    Use this when agents are added/removed/modified on disk.
    """
    global _agents_cache, _agents_cache_timestamp

    from src.agent_utils import discover_agents

    try:
        print("Manually refreshing agent cache...")
        old_count = len(_agents_cache) if _agents_cache else 0

        _agents_cache = discover_agents(settings.base_path)
        _agents_cache_timestamp = datetime.utcnow()

        print(f"✓ Cache refreshed: {len(_agents_cache)} agents discovered")

        return {
            "success": True,
            "message": "Agent cache refreshed",
            "previous_count": old_count,
            "current_count": len(_agents_cache),
            "timestamp": _agents_cache_timestamp.isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refresh cache: {str(e)}")


# ============================================================================
# VISUALIZATION ROUTES
# ============================================================================

@app.get("/api/agents/visualization/graph", response_model=AgentGraph)
async def get_agent_graph(db: Session = Depends(get_db)):
    """Get agent network graph for visualization"""
    agents = db.query(AgentDB).all()

    nodes = [
        AgentNode(
            id=agent.id,
            name=agent.name,
            tier=agent.tier,
            status=agent.status
        )
        for agent in agents
    ]

    edges = [
        AgentEdge(source=agent.reports_to, target=agent.id, type="manages")
        for agent in agents
        if agent.reports_to
    ]

    return AgentGraph(nodes=nodes, edges=edges)


@app.get("/api/agents/visualization/hierarchy", response_model=List[AgentHierarchy])
async def get_agent_hierarchy(db: Session = Depends(get_db)):
    """Get agent org chart hierarchy"""
    def build_hierarchy(agent: AgentDB) -> AgentHierarchy:
        children = db.query(AgentDB).filter(AgentDB.reports_to == agent.id).all()
        return AgentHierarchy(
            id=agent.id,
            name=agent.name,
            tier=agent.tier,
            status=agent.status,
            children=[build_hierarchy(child) for child in children]
        )

    # Get root agents (no reports_to)
    root_agents = db.query(AgentDB).filter(AgentDB.reports_to == None).all()
    return [build_hierarchy(agent) for agent in root_agents]


@app.get("/api/agents/visualization/kanban")
async def get_agent_kanban(db: Session = Depends(get_db)):
    """Get agents organized by status for Kanban board"""
    agents = db.query(AgentDB).all()

    kanban = {
        "idle": [],
        "working": [],
        "waiting": [],
        "error": [],
        "offline": []
    }

    for agent in agents:
        status_key = agent.status.value if hasattr(agent.status, 'value') else str(agent.status)
        if status_key in kanban:
            kanban[status_key].append({
                "id": agent.id,
                "name": agent.name,
                "tier": agent.tier.value if hasattr(agent.tier, 'value') else str(agent.tier),
                "last_active": agent.last_active.isoformat() if agent.last_active else None
            })

    return kanban


@app.get("/api/agents/visualization/grid")
async def get_agent_grid(db: Session = Depends(get_db)):
    """Get agents in grid/card format"""
    agents = db.query(AgentDB).all()

    return {
        "agents": [
            {
                "id": agent.id,
                "name": agent.name,
                "tier": agent.tier.value if hasattr(agent.tier, 'value') else str(agent.tier),
                "status": agent.status.value if hasattr(agent.status, 'value') else str(agent.status),
                "description": agent.description,
                "capabilities": agent.capabilities or [],
                "job_count": len(agent.jobs),
                "last_active": agent.last_active.isoformat() if agent.last_active else None
            }
            for agent in agents
        ]
    }


# ============================================================================
# CHAT ROUTES
# ============================================================================

@app.post("/api/chat", response_model=ChatResponse)
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
    context = [{"role": msg["role"], "content": msg["content"]} for msg in messages[-10:]]  # Last 10 messages

    # TODO: If use_rag is True, query RAG engine for relevant context
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


# ============================================================================
# TODOIST ROUTES
# ============================================================================

@app.post("/api/todoist/task", response_model=TodoistTaskResponse)
async def create_todoist_task(
    task: TodoistTaskCreate,
    db: Session = Depends(get_db)
):
    """Create Todoist task from agent"""
    agent = db.query(AgentDB).filter(AgentDB.id == task.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        result = create_task_for_andrew(
            content=task.content,
            description=task.description,
            project=task.project,
            priority=task.priority,
            due=task.due,
            labels=task.labels,
            agent=agent.name
        )

        if result.get("success"):
            return TodoistTaskResponse(
                success=True,
                task_id=result.get("task_id"),
                url=result.get("url"),
                message=result.get("message")
            )
        else:
            return TodoistTaskResponse(
                success=False,
                message=result.get("message", "Failed to create task")
            )

    except Exception as e:
        return TodoistTaskResponse(
            success=False,
            message=f"Error: {str(e)}"
        )


# ============================================================================
# JOB ROUTES (SIMPLIFIED FOR NOW)
# ============================================================================

@app.get("/api/jobs")
async def get_jobs(agent_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Get all jobs"""
    query = db.query(JobDB)
    if agent_id:
        query = query.filter(JobDB.agent_id == agent_id)
    jobs = query.all()
    return [Job.model_validate(job) for job in jobs]


# ============================================================================
# ACTIVITY ROUTES
# ============================================================================

@app.get("/api/activities")
async def get_activities(
    agent_id: Optional[int] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get recent activities"""
    query = db.query(ActivityDB)
    if agent_id:
        query = query.filter(ActivityDB.agent_id == agent_id)
    activities = query.order_by(ActivityDB.created_at.desc()).limit(limit).all()
    return [Activity.model_validate(activity) for activity in activities]


# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app_new:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
