"""
Agent API Routes - CRUD operations and visualization endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..database import get_db, AgentDB, AgentStatusEnum
from ..models import Agent, AgentCreate, AgentUpdate, AgentGraph, AgentNode, AgentEdge, AgentHierarchy

router = APIRouter(prefix="/agents")


@router.get("", response_model=List[Agent])
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


@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """Get specific agent"""
    agent = db.query(AgentDB).filter(AgentDB.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return Agent.model_validate(agent)


@router.post("", response_model=Agent)
async def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    """Create new agent"""
    db_agent = AgentDB(**agent.dict())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return Agent.model_validate(db_agent)


@router.put("/{agent_id}", response_model=Agent)
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


@router.post("/initialize")
async def initialize_agents(db: Session = Depends(get_db)):
    """Initialize agents - returns empty in production (agents managed via database)"""
    return {
        "success": True,
        "message": "Agents managed via database in production",
        "created": 0,
        "updated": 0
    }


# Visualization endpoints
@router.get("/visualization/graph", response_model=AgentGraph)
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


@router.get("/visualization/hierarchy", response_model=List[AgentHierarchy])
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

    root_agents = db.query(AgentDB).filter(AgentDB.reports_to == None).all()
    return [build_hierarchy(agent) for agent in root_agents]


@router.get("/visualization/kanban")
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


@router.get("/visualization/grid")
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
