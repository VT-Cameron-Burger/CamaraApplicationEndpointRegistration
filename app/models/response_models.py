"""
Response models for the CAMARA Application Endpoint Registration API.

This module contains all response models used for API endpoints,
using Pydantic v2 RootModel where appropriate for list responses.
"""

# Import from CamaraCommon
from CamaraCommon.Basic import XCorrelator
from pydantic import BaseModel, ConfigDict, Field, RootModel

# Import our existing models
from .application_endpoint import ApplicationEndpointsInfo
from .basic_types import ApplicationEndpointListId


class ApplicationEndpointList(BaseModel):
    """
    List of Application endpoints information deployed across various cloud zones.
    This is the main response model that combines the list ID with the endpoint info.
    """

    application_endpoint_list_id: ApplicationEndpointListId = Field(
        ..., alias="applicationEndpointListId"
    )
    application_endpoints_info: ApplicationEndpointsInfo = Field(
        ..., alias="applicationEndpointsInfo"
    )

    model_config = ConfigDict(populate_by_name=True)


class RegisterApplicationEndpointsResponse(BaseModel):
    """
    Response model for POST /application-endpoint-lists.
    Returns the applicationEndpointListId for the registered endpoints.
    """

    application_endpoint_list_id: ApplicationEndpointListId = Field(
        ..., alias="applicationEndpointListId"
    )

    model_config = ConfigDict(populate_by_name=True)


class GetApplicationEndpointsResponse(RootModel[list[ApplicationEndpointList]]):
    """
    Response model for GET /application-endpoint-lists.
    Returns an array of all registered ApplicationEndpointList objects.

    Using RootModel for clean array responses in Pydantic v2.
    """

    root: list[ApplicationEndpointList]


class GetApplicationEndpointsByIdResponse(BaseModel):
    """
    Response model for GET /application-endpoint-lists/{id}.
    Returns a specific ApplicationEndpointList by ID.
    """

    application_endpoint_list_id: ApplicationEndpointListId = Field(
        ..., alias="applicationEndpointListId"
    )
    application_endpoints_info: ApplicationEndpointsInfo = Field(
        ..., alias="applicationEndpointsInfo"
    )

    model_config = ConfigDict(populate_by_name=True)


# Common response wrappers with headers


class ApiResponseBase(BaseModel):
    """
    Base class for API responses that include common headers like x-correlator.
    """

    x_correlator: XCorrelator | None = Field(None, alias="x-correlator")

    model_config = ConfigDict(populate_by_name=True)


class RegisterApplicationEndpointsApiResponse(ApiResponseBase):
    """
    Complete API response for POST /application-endpoint-lists including headers.
    """

    data: RegisterApplicationEndpointsResponse = Field(...)


class GetApplicationEndpointsApiResponse(ApiResponseBase):
    """
    Complete API response for GET /application-endpoint-lists including headers.
    """

    data: GetApplicationEndpointsResponse = Field(...)


class GetApplicationEndpointsByIdApiResponse(ApiResponseBase):
    """
    Complete API response for GET /application-endpoint-lists/{id} including headers.
    """

    data: GetApplicationEndpointsByIdResponse = Field(...)


# Error response models (these will be enhanced in Task 15: CAMARA Error Handling)


class ErrorResponse(BaseModel):
    """
    Basic error response model. Will be enhanced with CAMARA-compliant errors later.
    """

    error: dict[str, str | int | bool] = Field(...)
    x_correlator: XCorrelator | None = Field(None, alias="x-correlator")

    model_config = ConfigDict(populate_by_name=True)
