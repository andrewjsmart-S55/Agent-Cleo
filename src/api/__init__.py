"""
Agent-Cleo API Routes Package
"""
from fastapi import APIRouter

# Create main API router
api_router = APIRouter(prefix="/api")

# Import and include sub-routers
from .agents import router as agents_router
from .jobs import router as jobs_router
from .activities import router as activities_router
from .chat import router as chat_router
from .todoist import router as todoist_router
from .health import router as health_router

api_router.include_router(agents_router, tags=["agents"])
api_router.include_router(jobs_router, tags=["jobs"])
api_router.include_router(activities_router, tags=["activities"])
api_router.include_router(chat_router, tags=["chat"])
api_router.include_router(todoist_router, tags=["todoist"])

__all__ = ["api_router", "health_router"]
