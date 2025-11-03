"""
Test the API endpoints to verify they exist and return NotImplementedError.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestApplicationEndpointRegistrationAPI:
    """Test the application endpoint registration API endpoints."""

    def test_register_application_endpoints_not_implemented(self):
        """Test that the register endpoint exists and returns 501."""
        response = client.post(
            "/api/v1/application-endpoint-registration/vwip/application-endpoint-lists",
            json={
                "application_endpoints_info": {
                    "applicationEndpoints": [],
                    "applicationProviderName": "TestProvider",
                    "applicationProfileId": {
                        "value": "123e4567-e89b-12d3-a456-426614174000"
                    }
                }
            }
        )
        assert response.status_code == 501
        assert "not yet implemented" in response.json()["detail"].lower()

    def test_get_all_application_endpoints_not_implemented(self):
        """Test that the get all endpoint exists and returns 501."""
        response = client.get(
            "/api/v1/application-endpoint-registration/vwip/application-endpoint-lists"
        )
        assert response.status_code == 501
        assert "not yet implemented" in response.json()["detail"].lower()

    def test_get_application_endpoints_by_id_not_implemented(self):
        """Test that the get by id endpoint exists and returns 501."""
        response = client.get(
            "/api/v1/application-endpoint-registration/vwip/application-endpoint-lists/123e4567-e89b-12d3-a456-426614174000"
        )
        assert response.status_code == 501
        assert "not yet implemented" in response.json()["detail"].lower()

    def test_update_application_endpoint_not_implemented(self):
        """Test that the update endpoint exists and returns 501."""
        response = client.put(
            "/api/v1/application-endpoint-registration/vwip/application-endpoint-lists/123e4567-e89b-12d3-a456-426614174000",
            json={
                "application_endpoints_info": {
                    "applicationEndpoints": [],
                    "applicationProviderName": "TestProvider",
                    "applicationProfileId": {
                        "value": "123e4567-e89b-12d3-a456-426614174000"
                    }
                }
            }
        )
        assert response.status_code == 501
        assert "not yet implemented" in response.json()["detail"].lower()

    def test_deregister_application_endpoint_not_implemented(self):
        """Test that the delete endpoint exists and returns 501."""
        response = client.delete(
            "/api/v1/application-endpoint-registration/vwip/application-endpoint-lists/123e4567-e89b-12d3-a456-426614174000"
        )
        assert response.status_code == 501
        assert "not yet implemented" in response.json()["detail"].lower()

    def test_x_correlator_header_support(self):
        """Test that endpoints accept x-correlator header."""
        response = client.get(
            "/api/v1/application-endpoint-registration/vwip/application-endpoint-lists",
            headers={"x-correlator": "test-correlation-id-123"}
        )
        # Should still return 501 but accept the header
        assert response.status_code == 501

    def test_api_documentation_includes_endpoints(self):
        """Test that the OpenAPI documentation includes our endpoints."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        openapi_doc = response.json()
        
        # Check that our endpoints are in the OpenAPI documentation
        paths = openapi_doc["paths"]
        assert "/api/v1/application-endpoint-registration/vwip/application-endpoint-lists" in paths
        assert "/api/v1/application-endpoint-registration/vwip/application-endpoint-lists/{application_endpoint_list_id}" in paths
        
        # Check that the correct methods are available
        endpoint_list_path = paths["/api/v1/application-endpoint-registration/vwip/application-endpoint-lists"]
        assert "get" in endpoint_list_path
        assert "post" in endpoint_list_path
        
        endpoint_by_id_path = paths["/api/v1/application-endpoint-registration/vwip/application-endpoint-lists/{application_endpoint_list_id}"]
        assert "get" in endpoint_by_id_path
        assert "put" in endpoint_by_id_path
        assert "delete" in endpoint_by_id_path