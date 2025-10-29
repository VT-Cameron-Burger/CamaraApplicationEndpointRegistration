"""
Test health endpoints
"""


def test_health_check(client):
    """Test basic health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["service"] == "Python HTTP API"


def test_detailed_health_check(client):
    """Test detailed health check endpoint"""
    response = client.get("/api/v1/health/detailed")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["service"] == "Python HTTP API"
    assert data["version"] == "1.0.0"
    assert "dependencies" in data


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["docs"] == "/docs"
