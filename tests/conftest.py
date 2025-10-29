"""
Test configuration and fixtures
"""

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.fixture
def sample_user():
    """Sample user data for testing"""
    return {"name": "John Doe", "email": "john.doe@example.com"}
