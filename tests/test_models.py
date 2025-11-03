"""
Comprehensive tests for all model validation.

This module tests:
- Model instantiation with valid data
- Field validation and constraints
- CamaraCommon integration
- Pydantic v2 RootModel behavior
- Error handling for invalid data
"""

from uuid import UUID, uuid4

import pytest
from CamaraCommon.Basic import XCorrelator
from CamaraCommon.Network import Port
from pydantic import ValidationError

from app.models.application_endpoint import (
    ApplicationEndpoint,
    ApplicationEndpointsInfo,
)
from app.models.basic_types import (
    ApplicationEndpointListId,
    ApplicationProfileId,
    DomainName,
    EdgeCloudProvider,
    EdgeCloudRegion,
    EdgeCloudZone,
    EdgeCloudZoneId,
    EdgeCloudZoneName,
    EdgeCloudZoneStatus,
    SingleIpv6Addr,
)
from app.models.request_models import (
    RegisterApplicationEndpointsRequest,
    UpdateApplicationEndpointRequest,
)
from app.models.response_models import (
    ApiResponseBase,
    ApplicationEndpointList,
    ErrorResponse,
    GetApplicationEndpointsApiResponse,
    GetApplicationEndpointsByIdResponse,
    GetApplicationEndpointsResponse,
    RegisterApplicationEndpointsApiResponse,
    RegisterApplicationEndpointsResponse,
)


class TestBasicTypes:
    """Test validation of basic type models."""

    def test_application_endpoint_list_id_valid(self):
        """Test valid ApplicationEndpointListId creation."""
        valid_uuid = uuid4()
        app_id = ApplicationEndpointListId(value=valid_uuid)
        assert app_id.value == valid_uuid

        # Test string UUID
        app_id_str = ApplicationEndpointListId(
            value=UUID("123e4567-e89b-12d3-a456-426614174000")
        )
        assert isinstance(app_id_str.value, UUID)

    def test_application_endpoint_list_id_invalid(self):
        """Test invalid ApplicationEndpointListId creation."""
        # Test with invalid UUID string (this should fail at UUID construction)
        with pytest.raises(ValueError):
            UUID("invalid-uuid")

    def test_application_profile_id_valid(self):
        """Test valid ApplicationProfileId creation."""
        valid_uuid = uuid4()
        profile_id = ApplicationProfileId(value=valid_uuid)
        assert profile_id.value == valid_uuid

    def test_domain_name_valid(self):
        """Test valid DomainName creation."""
        valid_domains = [
            "example.com",
            "sub.example.com",
            "test-domain.org",
            "a.b.c.d.com",
        ]

        for domain in valid_domains:
            domain_obj = DomainName(value=domain)
            assert domain_obj.value == domain

    def test_domain_name_invalid(self):
        """Test invalid DomainName creation."""
        invalid_domains = [
            "",
            ".",
            "example.",
            ".example.com",
            "ex ample.com",
            "example..com",
        ]

        for domain in invalid_domains:
            with pytest.raises(ValidationError):
                DomainName(value=domain)

    def test_edge_cloud_zone_id_valid(self):
        """Test valid EdgeCloudZoneId creation."""
        valid_uuid = uuid4()
        zone_id = EdgeCloudZoneId(value=valid_uuid)
        assert zone_id.value == valid_uuid

    def test_edge_cloud_zone_name_valid(self):
        """Test valid EdgeCloudZoneName creation."""
        zone_name = EdgeCloudZoneName(value="US-East-1")
        assert zone_name.value == "US-East-1"

    def test_edge_cloud_provider_valid(self):
        """Test valid EdgeCloudProvider creation."""
        provider = EdgeCloudProvider(value="AWS")
        assert provider.value == "AWS"

    def test_edge_cloud_region_valid(self):
        """Test valid EdgeCloudRegion creation."""
        region = EdgeCloudRegion(value="us-east-1")
        assert region.value == "us-east-1"

    def test_edge_cloud_zone_status_enum(self):
        """Test EdgeCloudZoneStatus enum values."""
        # Test valid enum values
        status1 = EdgeCloudZoneStatus.ACTIVE
        assert status1 == "active"

        status2 = EdgeCloudZoneStatus.INACTIVE
        assert status2 == "inactive"

        status3 = EdgeCloudZoneStatus.UNKNOWN
        assert status3 == "unknown"

        # Test invalid enum value
        with pytest.raises(ValueError):
            EdgeCloudZoneStatus("invalid-status")

    def test_single_ipv6_addr_valid(self):
        """Test valid SingleIpv6Addr creation."""
        valid_ipv6_addresses = [
            "2001:db8::1",
            "::1",
            "2001:db8:85a3::8a2e:370:7334",
            "fe80::1%lo0",
        ]

        for addr in valid_ipv6_addresses:
            ipv6_obj = SingleIpv6Addr(value=addr)
            assert ipv6_obj.value == addr

    def test_single_ipv6_addr_invalid(self):
        """Test invalid SingleIpv6Addr creation."""
        invalid_ipv6_addresses = [
            "192.168.1.1",  # IPv4
            "invalid-ip",
            "",
            "2001:db8::1::2",  # Invalid format
        ]

        for addr in invalid_ipv6_addresses:
            with pytest.raises(ValidationError):
                SingleIpv6Addr(value=addr)


class TestApplicationEndpointModels:
    """Test application endpoint related models."""

    def test_edge_cloud_zone_valid(self):
        """Test valid EdgeCloudZone creation."""
        zone_data = {
            "edgeCloudZoneId": EdgeCloudZoneId(value=uuid4()),
            "edgeCloudZoneName": EdgeCloudZoneName(value="US-East-1"),
            "edgeCloudProvider": EdgeCloudProvider(value="AWS"),
            "edgeCloudRegion": EdgeCloudRegion(value="us-east-1"),
            "edgeCloudZoneStatus": EdgeCloudZoneStatus.ACTIVE,
        }

        zone = EdgeCloudZone(**zone_data)
        assert zone.edge_cloud_zone_id == zone_data["edgeCloudZoneId"]
        assert zone.edge_cloud_zone_name == zone_data["edgeCloudZoneName"]
        assert zone.edge_cloud_provider == zone_data["edgeCloudProvider"]
        assert zone.edge_cloud_region == zone_data["edgeCloudRegion"]
        assert zone.edge_cloud_zone_status == EdgeCloudZoneStatus.ACTIVE

    def test_application_endpoint_valid(self):
        """Test valid ApplicationEndpoint creation."""
        endpoint_data = {
            "domainName": DomainName(value="api.example.com"),
            "port": Port(value=443),
            "edgeCloudZone": EdgeCloudZone(
                edgeCloudZoneId=EdgeCloudZoneId(value=uuid4()),
                edgeCloudZoneName=EdgeCloudZoneName(value="US-East-1"),
                edgeCloudProvider=EdgeCloudProvider(value="AWS"),
                edgeCloudRegion=EdgeCloudRegion(value="us-east-1"),
                edgeCloudZoneStatus=EdgeCloudZoneStatus.ACTIVE,
            ),
        }

        endpoint = ApplicationEndpoint(**endpoint_data)
        assert endpoint.domain_name is not None
        assert endpoint.domain_name.value == "api.example.com"
        assert endpoint.port.value == 443
        assert endpoint.edge_cloud_zone is not None
        assert endpoint.edge_cloud_zone.edge_cloud_zone_name.value == "US-East-1"

    def test_application_endpoint_port_validation(self):
        """Test port validation in ApplicationEndpoint."""
        base_data = {
            "domainName": DomainName(value="api.example.com"),
            "edgeCloudZone": EdgeCloudZone(
                edgeCloudZoneId=EdgeCloudZoneId(value=uuid4()),
                edgeCloudZoneName=EdgeCloudZoneName(value="US-East-1"),
                edgeCloudProvider=EdgeCloudProvider(value="AWS"),
                edgeCloudRegion=EdgeCloudRegion(value="us-east-1"),
                edgeCloudZoneStatus=EdgeCloudZoneStatus.ACTIVE,
            ),
        }

        # Valid ports
        valid_ports = [1, 80, 443, 8080, 65535]
        for port_val in valid_ports:
            endpoint = ApplicationEndpoint(**{
                **base_data, "port": Port(value=port_val)
            })
            assert endpoint.port.value == port_val

    def test_application_endpoints_info_valid(self):
        """Test valid ApplicationEndpointsInfo creation."""
        endpoints_data = {
            "applicationEndpoints": [
                ApplicationEndpoint(
                    domainName=DomainName(value="api.example.com"),
                    port=Port(value=443),
                    edgeCloudZone=EdgeCloudZone(
                        edgeCloudZoneId=EdgeCloudZoneId(value=uuid4()),
                        edgeCloudZoneName=EdgeCloudZoneName(value="US-East-1"),
                        edgeCloudProvider=EdgeCloudProvider(value="AWS"),
                        edgeCloudRegion=EdgeCloudRegion(value="us-east-1"),
                        edgeCloudZoneStatus=EdgeCloudZoneStatus.ACTIVE,
                    ),
                    **{},
                )
            ],
            "applicationProviderName": "TestProvider",
            "applicationProfileId": ApplicationProfileId(value=uuid4()),
        }

        endpoints_info = ApplicationEndpointsInfo(**endpoints_data)
        assert isinstance(endpoints_info.application_profile_id.value, UUID)
        assert len(endpoints_info.application_endpoints) == 1
        assert endpoints_info.application_endpoints[0].domain_name is not None
        assert (
            endpoints_info.application_endpoints[0].domain_name.value
            == "api.example.com"
        )

    def test_application_endpoints_info_empty_list(self):
        """Test ApplicationEndpointsInfo with empty endpoints list."""
        endpoints_data = {
            "applicationEndpoints": [],
            "applicationProviderName": "TestProvider",
            "applicationProfileId": ApplicationProfileId(value=uuid4()),
        }

        # Should allow empty list
        endpoints_info = ApplicationEndpointsInfo(**endpoints_data)
        assert len(endpoints_info.application_endpoints) == 0


class TestRequestModels:
    """Test API request models."""

    def test_register_application_endpoints_request_valid(self):
        """Test valid RegisterApplicationEndpointsRequest creation."""
        endpoints_info = ApplicationEndpointsInfo(
            applicationEndpoints=[
                ApplicationEndpoint(
                    domainName=DomainName(value="api.example.com"),
                    port=Port(value=443),
                    edgeCloudZone=EdgeCloudZone(
                        edgeCloudZoneId=EdgeCloudZoneId(value=uuid4()),
                        edgeCloudZoneName=EdgeCloudZoneName(value="US-East-1"),
                        edgeCloudProvider=EdgeCloudProvider(value="AWS"),
                        edgeCloudRegion=EdgeCloudRegion(value="us-east-1"),
                        edgeCloudZoneStatus=EdgeCloudZoneStatus.ACTIVE,
                    ),
                    **{},
                )
            ],
            applicationProviderName="TestProvider",
            applicationProfileId=ApplicationProfileId(value=uuid4()),
            **{},
        )

        request = RegisterApplicationEndpointsRequest(
            application_endpoints_info=endpoints_info
        )
        assert isinstance(request.application_endpoints_info, ApplicationEndpointsInfo)
        assert isinstance(
            request.application_endpoints_info.application_profile_id.value, UUID
        )

    def test_update_application_endpoint_request_valid(self):
        """Test valid UpdateApplicationEndpointRequest creation."""
        endpoints_info = ApplicationEndpointsInfo(
            applicationEndpoints=[
                ApplicationEndpoint(
                    domainName=DomainName(value="updated-api.example.com"),
                    port=Port(value=8080),
                    **{},
                    edgeCloudZone=EdgeCloudZone(
                        edgeCloudZoneId=EdgeCloudZoneId(value=uuid4()),
                        edgeCloudZoneName=EdgeCloudZoneName(value="US-West-1"),
                        edgeCloudProvider=EdgeCloudProvider(value="Azure"),
                        edgeCloudRegion=EdgeCloudRegion(value="us-west-1"),
                        edgeCloudZoneStatus=EdgeCloudZoneStatus.ACTIVE,
                    ),
                )
            ],
            applicationProviderName="TestProvider",
            **{},
            applicationProfileId=ApplicationProfileId(value=uuid4()),
        )

        request = UpdateApplicationEndpointRequest(
            application_endpoints_info=endpoints_info
        )
        assert isinstance(request.application_endpoints_info, ApplicationEndpointsInfo)
        assert (
            request.application_endpoints_info.application_endpoints[0].domain_name
            is not None
        )
        assert (
            request.application_endpoints_info.application_endpoints[
                0
            ].domain_name.value
            == "updated-api.example.com"
        )


class TestResponseModels:
    """Test API response models."""

    def test_application_endpoint_list_valid(self):
        """Test valid ApplicationEndpointList creation."""
        endpoints_info = ApplicationEndpointsInfo(
            applicationEndpoints=[
                ApplicationEndpoint(
                    domainName=DomainName(value="api.example.com"),
                    port=Port(value=443),
                    edgeCloudZone=EdgeCloudZone(
                        edgeCloudZoneId=EdgeCloudZoneId(value=uuid4()),
                        edgeCloudZoneName=EdgeCloudZoneName(value="US-East-1"),
                        edgeCloudProvider=EdgeCloudProvider(value="AWS"),
                        edgeCloudRegion=EdgeCloudRegion(value="us-east-1"),
                        edgeCloudZoneStatus=EdgeCloudZoneStatus.ACTIVE,
                    ),
                    **{},
                )
            ],
            applicationProviderName="TestProvider",
            applicationProfileId=ApplicationProfileId(value=uuid4()),
            **{},
        )

        list_data = {
            "applicationEndpointListId": ApplicationEndpointListId(value=uuid4()),
            "applicationEndpointsInfo": endpoints_info,
        }

        app_list = ApplicationEndpointList(**list_data)
        assert isinstance(app_list.application_endpoint_list_id.value, UUID)
        assert isinstance(app_list.application_endpoints_info, ApplicationEndpointsInfo)
        assert len(app_list.application_endpoints_info.application_endpoints) == 1

    def test_api_response_base_with_x_correlator(self):
        """Test ApiResponseBase with x-correlator header."""
        correlator = XCorrelator(value="test-correlation-id-123")
        response = ApiResponseBase(**{"x-correlator": correlator})
        assert response.x_correlator == correlator

    def test_api_response_base_without_x_correlator(self):
        """Test ApiResponseBase without x-correlator header."""
        response = ApiResponseBase(**{"x-correlator": None})
        assert response.x_correlator is None

    def test_error_response_valid(self):
        """Test valid ErrorResponse creation."""
        error_data = {
            "status": 400,
            "code": "INVALID_REQUEST",
            "message": "The request is invalid",
        }

        error = ErrorResponse(error=error_data, **{})
        assert error.error["status"] == 400
        assert error.error["code"] == "INVALID_REQUEST"
        assert error.error["message"] == "The request is invalid"

    def test_register_application_endpoints_response_valid(self):
        """Test valid RegisterApplicationEndpointsResponse creation."""
        response_data = {
            "applicationEndpointListId": ApplicationEndpointListId(value=uuid4())
        }
        response = RegisterApplicationEndpointsResponse(**response_data)
        assert isinstance(response.application_endpoint_list_id.value, UUID)

    def test_get_application_endpoints_response_valid(self):
        """Test valid GetApplicationEndpointsResponse creation."""
        endpoints_info = ApplicationEndpointsInfo(
            applicationEndpoints=[
                ApplicationEndpoint(
                    domainName=DomainName(value="api.example.com"),
                    port=Port(value=443),
                    edgeCloudZone=EdgeCloudZone(
                        edgeCloudZoneId=EdgeCloudZoneId(value=uuid4()),
                        edgeCloudZoneName=EdgeCloudZoneName(value="US-East-1"),
                        edgeCloudProvider=EdgeCloudProvider(value="AWS"),
                        edgeCloudRegion=EdgeCloudRegion(value="us-east-1"),
                        edgeCloudZoneStatus=EdgeCloudZoneStatus.ACTIVE,
                    ),
                    **{},
                )
            ],
            applicationProviderName="TestProvider",
            applicationProfileId=ApplicationProfileId(value=uuid4()),
            **{},
        )

        app_list = ApplicationEndpointList(
            applicationEndpointListId=ApplicationEndpointListId(value=uuid4()),
            applicationEndpointsInfo=endpoints_info,
        )

        response = GetApplicationEndpointsResponse(root=[app_list])
        assert len(response.root) == 1
        assert isinstance(response.root[0], ApplicationEndpointList)

    def test_get_application_endpoints_by_id_response_valid(self):
        """Test valid GetApplicationEndpointsByIdResponse creation."""
        endpoints_info = ApplicationEndpointsInfo(
            applicationEndpoints=[
                ApplicationEndpoint(
                    domainName=DomainName(value="api.example.com"),
                    port=Port(value=443),
                    edgeCloudZone=EdgeCloudZone(
                        edgeCloudZoneId=EdgeCloudZoneId(value=uuid4()),
                        edgeCloudZoneName=EdgeCloudZoneName(value="US-East-1"),
                        edgeCloudProvider=EdgeCloudProvider(value="AWS"),
                        edgeCloudRegion=EdgeCloudRegion(value="us-east-1"),
                        edgeCloudZoneStatus=EdgeCloudZoneStatus.ACTIVE,
                    ),
                    **{},
                )
            ],
            applicationProviderName="TestProvider",
            applicationProfileId=ApplicationProfileId(value=uuid4()),
            **{},
        )

        response_data = {
            "applicationEndpointListId": ApplicationEndpointListId(value=uuid4()),
            "applicationEndpointsInfo": endpoints_info,
        }

        response = GetApplicationEndpointsByIdResponse(**response_data)
        assert isinstance(response.application_endpoint_list_id.value, UUID)
        assert isinstance(response.application_endpoints_info, ApplicationEndpointsInfo)

    def test_api_response_models_with_x_correlator(self):
        """Test API response models with x-correlator integration."""
        correlator = XCorrelator(value="test-correlation-id-456")

        # Test RegisterApplicationEndpointsApiResponse
        register_response_data = RegisterApplicationEndpointsResponse(
            applicationEndpointListId=ApplicationEndpointListId(value=uuid4())
        )
        register_response = RegisterApplicationEndpointsApiResponse(
            data=register_response_data, **{"x-correlator": correlator}
        )
        assert register_response.x_correlator == correlator
        assert isinstance(
            register_response.data.application_endpoint_list_id.value, UUID
        )

        # Test GetApplicationEndpointsApiResponse
        get_response = GetApplicationEndpointsApiResponse(
            data=GetApplicationEndpointsResponse(root=[]),
            **{"x-correlator": correlator},
        )
        assert get_response.x_correlator == correlator
        assert len(get_response.data.root) == 0


class TestCamaraCommonIntegration:
    """Test integration with CamaraCommon types."""

    def test_x_correlator_import(self):
        """Test that XCorrelator can be imported and used."""
        correlator = XCorrelator(value="test-correlation-id")
        assert correlator.value == "test-correlation-id"

    def test_x_correlator_in_response_models(self):
        """Test XCorrelator usage in response models."""
        correlator = XCorrelator(value="integration-test-id")

        # Test that ApiResponseBase accepts XCorrelator
        response = ApiResponseBase(**{"x-correlator": correlator})
        assert response.x_correlator == correlator

        # Test serialization
        response_dict = response.model_dump()
        # The serialized field should use the Python field name, not the alias
        assert "x_correlator" in response_dict


class TestModelSerialization:
    """Test model serialization and deserialization."""

    def test_application_endpoint_serialization(self):
        """Test ApplicationEndpoint JSON serialization."""
        endpoint = ApplicationEndpoint(
            domainName=DomainName(value="api.example.com"),
            port=Port(value=443),
            edgeCloudZone=EdgeCloudZone(
                edgeCloudZoneId=EdgeCloudZoneId(value=uuid4()),
                edgeCloudZoneName=EdgeCloudZoneName(value="US-East-1"),
                edgeCloudProvider=EdgeCloudProvider(value="AWS"),
                edgeCloudRegion=EdgeCloudRegion(value="us-east-1"),
                edgeCloudZoneStatus=EdgeCloudZoneStatus.ACTIVE,
            ),
            **{},
        )

        serialized = endpoint.model_dump()

        # Check that serialization maintains structure (uses Python field names)
        assert serialized["domain_name"]["value"] == "api.example.com"
        assert serialized["port"]["value"] == 443
        assert (
            serialized["edge_cloud_zone"]["edge_cloud_zone_name"]["value"]
            == "US-East-1"
        )

    def test_root_model_serialization(self):
        """Test RootModel serialization behavior."""
        response = GetApplicationEndpointsResponse(root=[])

        # RootModel should serialize to its root value
        serialized = response.model_dump()
        assert isinstance(serialized, list)
        assert len(serialized) == 0


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_string_validation(self):
        """Test models handle empty strings appropriately."""
        with pytest.raises(ValidationError):
            DomainName(value="")

        with pytest.raises(ValidationError):
            EdgeCloudZoneName(value="")

    def test_unicode_handling(self):
        """Test models handle Unicode characters appropriately."""
        # Domain names with international characters should be handled properly
        unicode_domain = "xn--nxasmq6b.com"  # IDN domain
        domain = DomainName(value=unicode_domain)
        assert domain.value == unicode_domain
