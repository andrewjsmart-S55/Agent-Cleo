"""
Health Check API Route
"""
from fastapi import APIRouter

from ..config import settings
from ..models import HealthCheck
from ..overlord_client.client import get_overlord_client

router = APIRouter()


@router.get("/health", response_model=HealthCheck)
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
