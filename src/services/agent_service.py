"""
Agent Service - Business logic for agent operations
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..database import AgentDB, AgentStatusEnum


class AgentService:
    """Service class for agent-related business logic"""

    @staticmethod
    def get_agents_by_tier(db: Session, tier: str) -> List[AgentDB]:
        """Get all agents of a specific tier"""
        return db.query(AgentDB).filter(AgentDB.tier == tier).all()

    @staticmethod
    def get_active_agents(db: Session) -> List[AgentDB]:
        """Get all agents that are not offline"""
        return db.query(AgentDB).filter(
            AgentDB.status != AgentStatusEnum.OFFLINE
        ).all()

    @staticmethod
    def update_agent_status(
        db: Session,
        agent_id: int,
        status: AgentStatusEnum
    ) -> Optional[AgentDB]:
        """Update agent status and last active timestamp"""
        agent = db.query(AgentDB).filter(AgentDB.id == agent_id).first()
        if agent:
            agent.status = status
            agent.last_active = datetime.utcnow()
            db.commit()
        return agent

    @staticmethod
    def get_agent_hierarchy(db: Session, agent_id: int) -> dict:
        """Get agent with all subordinates recursively"""
        agent = db.query(AgentDB).filter(AgentDB.id == agent_id).first()
        if not agent:
            return {}

        return {
            "id": agent.id,
            "name": agent.name,
            "tier": agent.tier.value,
            "status": agent.status.value,
            "subordinates": [
                AgentService.get_agent_hierarchy(db, sub.id)
                for sub in agent.subordinates
            ]
        }

    @staticmethod
    def get_agent_stats(db: Session) -> dict:
        """Get aggregated stats across all agents"""
        total = db.query(AgentDB).count()
        by_status = {}
        for status in AgentStatusEnum:
            count = db.query(AgentDB).filter(AgentDB.status == status).count()
            by_status[status.value] = count

        by_tier = {}
        agents = db.query(AgentDB).all()
        for agent in agents:
            tier = agent.tier.value
            by_tier[tier] = by_tier.get(tier, 0) + 1

        return {
            "total": total,
            "by_status": by_status,
            "by_tier": by_tier
        }
