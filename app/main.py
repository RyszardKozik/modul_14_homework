import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import engine
from app.models import Base
from app.routers import auth, users, contacts
from app.routers.users import router as users_router
from app.routers.contacts import router as contacts_router
from app.views import router as views_router
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# Middleware configuration for CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables in the database if they don't exist
Base.metadata.create_all(bind=engine)

# Include routers for different endpoints
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
app.include_router(views_router)

@app.get("/")
def read_main():
    """
    Root endpoint.

    Returns:
        dict: A greeting message.
    """
    return {"message": "Welcome to the API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
