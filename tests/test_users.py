import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }

def test_register_user(test_user):
    response = client.post("/register", json=test_user)
    assert response.status_code == 201
    assert response.json()["email"] == test_user["email"]
    assert "id" in response.json()

def test_login_user(test_user):
    # First, register the user
    client.post("/register", json=test_user)
    
    # Then, log in
    response = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_get_user_details(test_user):
    # First, register the user and log in to get the token
    client.post("/register", json=test_user)
    login_response = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    token = login_response.json()["access_token"]

    # Get user details
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]

def test_invalid_login():
    response = client.post("/login", data={"username": "invalid@example.com", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
