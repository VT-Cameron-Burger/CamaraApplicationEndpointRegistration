"""
Request models for the CAMARA Application Endpoint Registration API.

This module contains all request models used for API endpoints.
"""

from pydantic import BaseModel, ConfigDict, Field

# Import our existing models
from .application_endpoint import ApplicationEndpointsInfo


class RegisterApplicationEndpointsRequest(BaseModel):
    """
    Request model for POST /application-endpoint-lists.
    Accepts ApplicationEndpointsInfo to register new endpoints.
    """

    application_endpoints_info: ApplicationEndpointsInfo = Field(...)

    model_config = ConfigDict(populate_by_name=True)


class UpdateApplicationEndpointRequest(BaseModel):
    """
    Request model for PUT /application-endpoint-lists/{id}.
    Accepts updated ApplicationEndpointsInfo.
    """

    application_endpoints_info: ApplicationEndpointsInfo = Field(...)

    model_config = ConfigDict(populate_by_name=True)
