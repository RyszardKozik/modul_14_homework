from app.auth_utils import verify_password, get_password_hash, create_access_token, create_refresh_token
from datetime import timedelta

def test_password_hashing():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password)

def test_token_creation():
    data = {"sub": "testuser"}
    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)
    assert access_token is not None
    assert refresh_token is not None

if __name__ == "__main__":
    test_password_hashing()
    test_token_creation()
    print("All tests passed.")
