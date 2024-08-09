from fastapi.testclient import TestClient
from app.main import app  # assuming your FastAPI app is created in main.py

client = TestClient(app)

def test_get_current_user():
    response = client.get("/users/me", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200
    assert response.json() == {"username": "testuser"}  # Adjust based on expected response

if __name__ == "__main__":
    test_get_current_user()
    print("Functional test passed.")
