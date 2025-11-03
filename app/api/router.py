"""
Main API router configuration.

This module sets up the main API router for the CAMARA Application Endpoint Registration API.
"""

from fastapi import APIRouter

from app.api.endpoints import application_endpoint_registration

# Create the main API router
api_router = APIRouter()

# Include the application endpoint registration router
api_router.include_router(
    application_endpoint_registration.router,
    tags=["Application Endpoint Registration"]
)