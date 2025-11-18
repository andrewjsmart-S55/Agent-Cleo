"""
Job API Routes - Task management endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db, JobDB
from ..models import Job

router = APIRouter(prefix="/jobs")


@router.get("")
async def get_jobs(agent_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Get all jobs with optional agent filtering"""
    query = db.query(JobDB)
    if agent_id:
        query = query.filter(JobDB.agent_id == agent_id)
    jobs = query.all()
    return [Job.model_validate(job) for job in jobs]
