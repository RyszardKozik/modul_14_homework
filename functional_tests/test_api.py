import sys
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Add the 'app' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

# Create a TestClient instance to make requests to the FastAPI app
client = TestClient(app)

def test_example_endpoint():
    response = client.get("/example-endpoint")  # Adjust according to your routes
    assert response.status_code == 200

def test_create_user():
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

def test_login_user():
    # First, create a user
    client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )

    # Then, log in the user
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_user_info():
    # First, create and log in a user to get the token
    client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    login_response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = login_response.json().get("access_token")

    # Use the token to get user info
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
