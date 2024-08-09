import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

# Debugging step: Print the current Python path
print(f"Project root added to sys.path: {project_root}")
print(f"Current sys.path: {sys.path}")

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError
from app import crud, schemas, models
from app.db import get_db
from app.auth_utils import create_access_token, decode_token, get_password_hash, verify_password
from app.email_utils import send_reset_password_email
from app.config import settings
from app.models import User

# Define the API router
router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define the OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint to log in a user.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing username and password.
        db (Session): Database session dependency.

    Returns:
        dict: JWT access token.
    """
    user = crud.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh", response_model=schemas.Token)
async def refresh_token(token: str, db: Session = Depends(get_db)):
    """
    Endpoint to refresh the JWT token.

    Args:
        token (str): The current JWT token.
        db (Session): Database session dependency.

    Returns:
        dict: New JWT access token.
    """
    try:
        # Decode the current token to extract user information
        payload = decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Fetch the user from the database
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check if the user is still active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )

        # Optionally, check for specific permissions
        if not user.has_permission("refresh_token"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have permission to refresh token",
            )

        # Create a new access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": new_access_token, "token_type": "bearer"}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/reset-password")
async def reset_password(email: str, db: Session = Depends(get_db)):
    """
    Endpoint to initiate the password reset process.

    Args:
        email (str): The user's email.
        db (Session): Database session dependency.

    Returns:
        dict: A success message.
    """
    # Fetch the user from the database by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email not found.",
        )

    # Ensure the user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user.",
        )

    # Create a reset token
    reset_token_expires = timedelta(hours=settings.RESET_TOKEN_EXPIRE_HOURS)
    reset_token = create_access_token(
        data={"sub": user.email}, expires_delta=reset_token_expires
    )

    # Send reset password email
    try:
        send_reset_password_email(email=user.email, token=reset_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send reset password email.",
        )

    return {"message": "Password reset email sent successfully."}
