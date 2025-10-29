"""
Test user endpoints
"""


def test_create_user(client, sample_user):
    """Test creating a new user"""
    response = client.post("/api/v1/users", json=sample_user)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == sample_user["name"]
    assert data["email"] == sample_user["email"]
    assert data["is_active"] is True
    assert "id" in data


def test_get_users(client, sample_user):
    """Test getting all users"""
    # First create a user
    client.post("/api/v1/users", json=sample_user)

    # Then get all users
    response = client.get("/api/v1/users")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_user_by_id(client, sample_user):
    """Test getting a user by ID"""
    # First create a user
    create_response = client.post("/api/v1/users", json=sample_user)
    user_id = create_response.json()["id"]

    # Then get the user by ID
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == sample_user["name"]
    assert data["email"] == sample_user["email"]


def test_get_nonexistent_user(client):
    """Test getting a non-existent user"""
    response = client.get("/api/v1/users/999")
    assert response.status_code == 404


def test_update_user(client, sample_user):
    """Test updating a user"""
    # First create a user
    create_response = client.post("/api/v1/users", json=sample_user)
    user_id = create_response.json()["id"]

    # Update the user
    updated_data = {"name": "Jane Doe", "email": "jane.doe@example.com"}
    response = client.put(f"/api/v1/users/{user_id}", json=updated_data)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["email"] == updated_data["email"]


def test_delete_user(client, sample_user):
    """Test deleting a user"""
    # First create a user
    create_response = client.post("/api/v1/users", json=sample_user)
    user_id = create_response.json()["id"]

    # Delete the user
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data

    # Verify user is deleted
    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404


def test_create_user_duplicate_email(client, sample_user):
    """Test creating a user with duplicate email"""
    # Create first user
    client.post("/api/v1/users", json=sample_user)

    # Try to create another user with same email
    response = client.post("/api/v1/users", json=sample_user)
    assert response.status_code == 400

    data = response.json()
    assert "Email already registered" in data["detail"]
