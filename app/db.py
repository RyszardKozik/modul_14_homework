from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create the SQLAlchemy engine using the database URL from settings
engine = create_engine(settings.database_url)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for our models to inherit from
Base = declarative_base()

# Dependency for getting the database session
def get_db():
    """
    Dependency for getting the database session.

    Yields:
        Session: A new database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
