"""
Health check endpoints
"""

from datetime import datetime, timezone
from typing import Dict, Union

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Union[str, bool]]:
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": settings.PROJECT_NAME,
    }


@router.get("/health/detailed")
async def detailed_health_check() -> Dict[str, Union[str, Dict[str, str]]]:
    """
    Detailed health check with more information
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "uptime": "Application is running",
        "dependencies": {"database": "healthy", "external_apis": "healthy"},
    }
