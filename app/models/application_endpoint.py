"""
Application-specific models for the CAMARA Application Endpoint Registration API.

This module contains the application endpoint models including ApplicationEndpoint,
ApplicationEndpointsInfo, and API request/response models.
"""

# Import types from CamaraCommon
from CamaraCommon.Network import Port, SingleIpv4Addr
from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

# Import basic types
from .basic_types import (
    ApplicationProfileId,
    DomainName,
    EdgeCloudZone,
    SingleIpv6Addr,
)


class ApplicationEndpoint(BaseModel):
    """
    An application server IP address or FQDN with a port, exposed by an
    application instance deployed on the Edge Cloud Zone.
    """

    domain_name: DomainName | None = Field(None, alias="domainName")
    ipv4_address: SingleIpv4Addr | None = Field(None, alias="ipv4Address")
    ipv6_address: SingleIpv6Addr | None = Field(None, alias="ipv6Address")
    port: Port
    edge_cloud_zone: EdgeCloudZone | None = Field(None, alias="edgeCloudZone")
    application_endpoint_description: str | None = Field(
        None,
        alias="applicationEndpointDescription",
        examples=["V2X app deployed at ZoneA"],
    )

    @field_validator("domain_name", "ipv4_address", "ipv6_address", mode="before")
    @classmethod
    def validate_address_fields(
        cls,
        v: DomainName | SingleIpv4Addr | SingleIpv6Addr | None,
        info: ValidationInfo,
    ) -> DomainName | SingleIpv4Addr | SingleIpv6Addr | None:
        """Ensure exactly one of domain_name, ipv4_address, or ipv6_address is provided"""
        # This will be handled by the root validator
        return v

    def model_post_init(self, __context: dict[str, object] | None) -> None:
        """Validate that exactly one address type is provided"""
        address_fields = [
            self.domain_name is not None,
            self.ipv4_address is not None,
            self.ipv6_address is not None,
        ]

        if sum(address_fields) != 1:
            raise ValueError(
                "Exactly one of domain_name, ipv4_address, or ipv6_address must be"
                " provided"
            )

    model_config = ConfigDict(populate_by_name=True)


class ApplicationEndpointsInfo(BaseModel):
    """
    Endpoint information of the Application deployed across different
    Edge Cloud Zones.
    """

    application_endpoints: list[ApplicationEndpoint] = Field(
        ...,
        alias="applicationEndpoints",
        description=(
            "List of endpoints of the application deployed across various Edge Cloud"
            " Zones"
        ),
    )
    application_provider_name: str = Field(
        ..., alias="applicationProviderName", examples=["AppProvider"]
    )
    application_description: str | None = Field(
        None, alias="applicationDescription", examples=["This is a V2X application."]
    )
    application_profile_id: ApplicationProfileId = Field(
        ..., alias="applicationProfileId"
    )

    model_config = ConfigDict(populate_by_name=True)
