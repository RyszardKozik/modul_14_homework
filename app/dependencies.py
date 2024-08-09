from sqlalchemy.orm import Session
from app.db import SessionLocal

# Dependency for getting the database session
def get_db():
    """
    Provides a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
