"""
Activity API Routes - Activity logging endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db, ActivityDB
from ..models import Activity

router = APIRouter(prefix="/activities")


@router.get("")
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
