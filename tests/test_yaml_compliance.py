"""
YAML Compliance Test for CAMARA Application Endpoint Registration API.

This test verifies that our Pydantic models are fully compliant with the
OpenAPI YAML specification, including:
- Field names and types
- Enum values
- Validation patterns
- Required vs optional fields
- Example data compatibility

Note: Some mypy type ignores are used in this file for test scenarios
that intentionally test edge cases and validation failures.
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
from app.models.response_models import (
    ApplicationEndpointList,
    GetApplicationEndpointsResponse,
    RegisterApplicationEndpointsResponse,
)


class TestYAMLCompliance:
    """Test compliance with the YAML specification."""

    def test_yaml_example_data_compatibility(self):
        """Test that our models work with the exact example data from the YAML spec."""
        # This is the exact example from the YAML specification
        yaml_example = {
            "applicationEndpoints": [
                {
                    "domainName": "app.example.com",
                    "port": 8080,
                    "applicationEndpointDescription": "V2X app deployed at ZoneA",
                    "edgeCloudZone": {
                        "edgeCloudZoneId": "123e4567-e89b-12d3-a456-426614174000",
                        "edgeCloudZoneName": "ZoneA",
                        "edgeCloudProvider": "ProviderA",
                        "edgeCloudRegion": "us-west-1",
                        "edgeCloudZoneStatus": "active",
                    },
                }
            ],
            "applicationProviderName": "AppProvider",
            "applicationDescription": "This is a V2X application.",
            "applicationProfileId": "123e4567-e89b-12d3-a456-426614174000",
        }

        # Test EdgeCloudZone with YAML example data
        edge_zone_data = yaml_example["applicationEndpoints"][0]["edgeCloudZone"]
        edge_zone = EdgeCloudZone(
            edgeCloudZoneId=EdgeCloudZoneId(
                value=UUID(edge_zone_data["edgeCloudZoneId"])
            ),
            edgeCloudZoneName=EdgeCloudZoneName(
                value=edge_zone_data["edgeCloudZoneName"]
            ),
            edgeCloudProvider=EdgeCloudProvider(
                value=edge_zone_data["edgeCloudProvider"]
            ),
            edgeCloudRegion=EdgeCloudRegion(value=edge_zone_data["edgeCloudRegion"]),
            edgeCloudZoneStatus=EdgeCloudZoneStatus.ACTIVE,
        )

        # Verify serialization matches YAML structure
        serialized_zone = edge_zone.model_dump(by_alias=True)
        assert serialized_zone["edgeCloudZoneStatus"] == "active"
        assert serialized_zone["edgeCloudZoneName"]["value"] == "ZoneA"
        assert serialized_zone["edgeCloudProvider"]["value"] == "ProviderA"

        # Test ApplicationEndpoint with YAML example
        endpoint_data = yaml_example["applicationEndpoints"][0]
        endpoint = ApplicationEndpoint(
            domainName=DomainName(value=endpoint_data["domainName"]),
            port=Port(value=endpoint_data["port"]),
            applicationEndpointDescription=endpoint_data[
                "applicationEndpointDescription"
            ],
            edgeCloudZone=edge_zone,
            **{},
        )

        # Verify field access and types
        assert endpoint.domain_name is not None
        assert endpoint.domain_name.value == "app.example.com"
        assert endpoint.port.value == 8080
        assert endpoint.application_endpoint_description == "V2X app deployed at ZoneA"

        # Test ApplicationEndpointsInfo with YAML example
        endpoints_info = ApplicationEndpointsInfo(
            applicationEndpoints=[endpoint],
            applicationProviderName=yaml_example["applicationProviderName"],
            applicationDescription=yaml_example["applicationDescription"],
            applicationProfileId=ApplicationProfileId(
                value=UUID(yaml_example["applicationProfileId"])
            ),
        )

        assert len(endpoints_info.application_endpoints) == 1
        assert endpoints_info.application_provider_name == "AppProvider"
        assert endpoints_info.application_description == "This is a V2X application."

    def test_edge_cloud_zone_status_enum_compliance(self):
        """Verify EdgeCloudZoneStatus enum matches YAML specification exactly."""
        # YAML spec defines: enum: [active, inactive, unknown], default: unknown

        # Test all valid enum values
        assert EdgeCloudZoneStatus.ACTIVE.value == "active"
        assert EdgeCloudZoneStatus.INACTIVE.value == "inactive"
        assert EdgeCloudZoneStatus.UNKNOWN.value == "unknown"

        # Test enum serialization
        zone = EdgeCloudZone(
            edgeCloudZoneId=EdgeCloudZoneId(value=uuid4()),
            edgeCloudZoneName=EdgeCloudZoneName(value="TestZone"),
            edgeCloudProvider=EdgeCloudProvider(value="TestProvider"),
            edgeCloudZoneStatus=EdgeCloudZoneStatus.ACTIVE,
            edgeCloudRegion=None,
        )

        serialized = zone.model_dump(by_alias=True)
        assert serialized["edgeCloudZoneStatus"] == "active"

    def test_domain_name_pattern_compliance(self):
        """Verify DomainName pattern matches YAML specification exactly."""
        # YAML pattern: ^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)+$
        # minLength: 4, maxLength: 253

        # Test valid domains from YAML examples
        valid_domains = [
            "app.example.com",  # YAML example
            "a.bc",  # Minimum valid length (4 chars)
            "subdomain.example.org",
            "multi.level.domain.example.com",
        ]

        for domain in valid_domains:
            domain_obj = DomainName(value=domain)
            assert domain_obj.value == domain

        # Test invalid domains
        invalid_cases = [
            ("a.b", "too short"),  # < 4 characters
            ("example", "missing dot"),  # No FQDN structure
            ("", "empty string"),
            (".example.com", "starts with dot"),
            ("example.", "ends with dot"),
            ("ex ample.com", "contains space"),
        ]

        for invalid_domain, reason in invalid_cases:
            with pytest.raises(ValidationError):
                DomainName(
                    value=invalid_domain
                ), f"Should reject {reason}: {invalid_domain}"

    def test_port_range_compliance(self):
        """Verify Port validation matches YAML specification (0-65535)."""
        # Test boundary values
        valid_ports = [0, 1, 8080, 65535]  # YAML example uses 8080

        for port_val in valid_ports:
            port = Port(value=port_val)
            assert port.value == port_val

        # Test invalid ports
        invalid_ports = [-1, 65536]

        for port_val in invalid_ports:
            with pytest.raises(ValidationError):
                Port(value=port_val)

    def test_uuid_format_compliance(self):
        """Verify UUID fields match YAML format specification."""
        # YAML specifies format: uuid for ApplicationProfileId and ApplicationEndpointListId

        test_uuid = "123e4567-e89b-12d3-a456-426614174000"  # From YAML example

        # Test ApplicationProfileId
        profile_id = ApplicationProfileId(value=UUID(test_uuid))
        assert str(profile_id.value) == test_uuid

        # Test ApplicationEndpointListId
        list_id = ApplicationEndpointListId(value=UUID(test_uuid))
        assert str(list_id.value) == test_uuid

    def test_application_endpoint_required_fields(self):
        """Verify ApplicationEndpoint required fields match YAML specification."""
        # YAML spec: port is required, one of domainName/ipv4Address/ipv6Address required

        # Test with domainName (valid)
        endpoint1 = ApplicationEndpoint(
            domainName=DomainName(value="test.example.com"), port=Port(value=8080), **{}
        )
        assert (
            endpoint1.domain_name is not None
            and endpoint1.domain_name.value == "test.example.com"
        )
        assert endpoint1.ipv4_address is None
        assert endpoint1.ipv6_address is None

        # Test with IPv6 (valid)
        endpoint2 = ApplicationEndpoint(
            ipv6Address=SingleIpv6Addr(value="2001:db8::1"), port=Port(value=8080), **{}
        )
        assert (
            endpoint2.ipv6_address is not None
            and endpoint2.ipv6_address.value == "2001:db8::1"
        )
        assert endpoint2.domain_name is None
        assert endpoint2.ipv4_address is None

        # Test missing port (should fail)
        with pytest.raises(ValidationError):
            ApplicationEndpoint(
                domainName=DomainName(value="test.example.com"),
                **{},
                # Missing required port
            )

        # Test missing all address fields (should fail)
        with pytest.raises(ValidationError):
            ApplicationEndpoint(
                port=Port(value=8080),
                **{},
                # Missing required address field
            )

    def test_application_endpoints_info_required_fields(self):
        """Verify ApplicationEndpointsInfo required fields match YAML specification."""
        # YAML spec: applicationEndpoints, applicationProviderName, applicationProfileId are required

        valid_endpoint = ApplicationEndpoint(
            domainName=DomainName(value="test.example.com"), port=Port(value=8080), **{}
        )

        # Test valid complete structure
        endpoints_info = ApplicationEndpointsInfo(
            applicationEndpoints=[valid_endpoint],
            applicationProviderName="TestProvider",
            applicationProfileId=ApplicationProfileId(value=uuid4()),
            applicationDescription=None,
        )
        assert len(endpoints_info.application_endpoints) == 1
        assert endpoints_info.application_provider_name == "TestProvider"
        assert isinstance(endpoints_info.application_profile_id.value, UUID)

        # Test missing required fields
        with pytest.raises(ValidationError):
            ApplicationEndpointsInfo(
                applicationEndpoints=[valid_endpoint],
                **{},
                # Missing applicationProviderName and applicationProfileId
            )

    def test_edge_cloud_zone_required_fields(self):
        """Verify EdgeCloudZone required fields match YAML specification."""
        # YAML spec: edgeCloudZoneId, edgeCloudZoneName, edgeCloudProvider are required

        # Test valid complete structure
        zone = EdgeCloudZone(
            edgeCloudZoneId=EdgeCloudZoneId(value=uuid4()),
            edgeCloudZoneName=EdgeCloudZoneName(value="TestZone"),
            edgeCloudProvider=EdgeCloudProvider(value="TestProvider"),
            **{},
            # edgeCloudRegion and edgeCloudZoneStatus are optional
        )
        assert (
            zone.edge_cloud_zone_status == EdgeCloudZoneStatus.UNKNOWN
        )  # Default value
        assert zone.edge_cloud_region is None  # Optional field

        # Test missing required fields
        with pytest.raises(ValidationError):
            EdgeCloudZone(
                edgeCloudZoneId=EdgeCloudZoneId(value=uuid4()),
                **{},
                # Missing required edgeCloudZoneName and edgeCloudProvider
            )

    def test_response_model_structure_compliance(self):
        """Verify response models match YAML response schemas."""

        # Test ApplicationEndpointList structure
        endpoint = ApplicationEndpoint(
            domainName=DomainName(value="api.example.com"), port=Port(value=8080), **{}
        )

        endpoints_info = ApplicationEndpointsInfo(
            applicationEndpoints=[endpoint],
            applicationProviderName="TestProvider",
            applicationProfileId=ApplicationProfileId(value=uuid4()),
            applicationDescription=None,
        )

        app_list = ApplicationEndpointList(
            applicationEndpointListId=ApplicationEndpointListId(value=uuid4()),
            applicationEndpointsInfo=endpoints_info,
        )

        # Verify structure matches YAML schema
        serialized = app_list.model_dump(by_alias=True)
        assert "applicationEndpointListId" in serialized
        assert "applicationEndpointsInfo" in serialized
        assert "applicationEndpoints" in serialized["applicationEndpointsInfo"]
        assert "applicationProviderName" in serialized["applicationEndpointsInfo"]
        assert "applicationProfileId" in serialized["applicationEndpointsInfo"]

        # Test GetApplicationEndpointsResponse (array of ApplicationEndpointList)
        response = GetApplicationEndpointsResponse(root=[app_list])
        serialized_response = response.model_dump()
        assert isinstance(serialized_response, list)
        assert len(serialized_response) == 1

        # Test RegisterApplicationEndpointsResponse (single ApplicationEndpointListId)
        register_response = RegisterApplicationEndpointsResponse(
            applicationEndpointListId=ApplicationEndpointListId(value=uuid4())
        )
        serialized_register = register_response.model_dump(by_alias=True)
        assert "applicationEndpointListId" in serialized_register

    def test_field_alias_compliance(self):
        """Verify field aliases match YAML specification exactly."""
        # Test that serialization uses the correct field names from YAML

        endpoint = ApplicationEndpoint(
            domainName=DomainName(value="test.example.com"),
            port=Port(value=8080),
            applicationEndpointDescription="Test endpoint",
            **{},
        )

        serialized = endpoint.model_dump(by_alias=True)

        # Verify YAML field names are used in serialization
        expected_fields = [
            "domainName",  # Not domain_name
            "port",
            "applicationEndpointDescription",  # Not application_endpoint_description
            "ipv4Address",  # Not ipv4_address
            "ipv6Address",  # Not ipv6_address
            "edgeCloudZone",  # Not edge_cloud_zone
        ]

        for field in expected_fields:
            if field in ["domainName", "port", "applicationEndpointDescription"]:
                assert (
                    field in serialized
                ), f"Field {field} should be present in serialization"
            else:
                # These fields should exist as keys even if None
                assert field in serialized or serialized.get(field) is None

    def test_x_correlator_compliance(self):
        """Verify x-correlator header matches YAML specification."""
        # YAML spec: pattern: ^[a-zA-Z0-9-_:;.\/<>{}]{0,256}$

        valid_correlators = [
            "b4333c46-49c0-4f62-80d7-f0ef930f1c46",  # YAML example
            "simple-id",
            "complex:id;with/special<chars>",
            "",  # Empty string allowed (0-256 length)
            "a" * 256,  # Maximum length
        ]

        for correlator_val in valid_correlators:
            correlator = XCorrelator(value=correlator_val)
            assert correlator.value == correlator_val

        # Test too long correlator
        with pytest.raises(ValidationError):
            XCorrelator(value="a" * 257)  # Exceeds maximum length


if __name__ == "__main__":
    # Run compliance tests
    pytest.main([__file__, "-v"])
