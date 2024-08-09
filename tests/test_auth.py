import pytest
from fastapi.testclient import TestClient
from app.main import app  
from app.config import settings  

client = TestClient(app)

def test_register_user():
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email": "testuser@example.com"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

def test_login_user():
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_protected_route():
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    token = response.json()["access_token"]

    # Without token
    response = client.get("/protected-route")
    assert response.status_code == 401

    # With token
    response = client.get("/protected-route", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "You are authenticated"}

def test_refresh_token():
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    refresh_token = response.json()["refresh_token"]

    response = client.post("/auth/refresh", headers={
        "Authorization": f"Bearer {refresh_token}"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_invalid_login():
    response = client.post("/auth/login", data={
        "username": "wronguser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
