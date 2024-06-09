"""
Imports for setting up a FastAPI application with SQLAlchemy database integration.

Imports:
    - os: Provides functions for interacting with the operating system.
    - FastAPI: A modern, fast (high-performance) web framework for building APIs with Python.
    - HTTPException: Exception to return as an HTTP response.
    - Depends: A decorator for dependencies.
    - BaseModel: Base class for creating Pydantic models.
    - EmailStr: Email validation string type from Pydantic.
    - create_engine: Function to create a SQLAlchemy engine.
    - Column: Class to represent a column in a database table.
    - Integer: Integer data type from SQLAlchemy.
    - String: String data type from SQLAlchemy.
    - TIMESTAMP: TIMESTAMP data type from SQLAlchemy.
    - func: Module for SQL functions in SQLAlchemy.
    - declarative_base: Function for creating a base class for declarative class definitions.
    - sessionmaker: Function for creating a session factory in SQLAlchemy.
    - Session: Represents a database session in SQLAlchemy.
    - datetime: Module for manipulating dates and times.
    - uvicorn: ASGI server implementation, used for running the FastAPI application.

Note: Ensure you have the necessary packages installed to use these imports.
"""
from datetime import datetime
import os
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func # pylint: disable=unused-import
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import Session



DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_URL')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = SessionLocal()
Base = declarative_base()

# Create tables in the database
#Base.metadata.create_all(bind=engine)


# Pydantic model for user creation
class UsuarioCreate(BaseModel):
    """Pydantic model for creating a new user"""

    id: int
    email: EmailStr
    name: str
    gender: str
    birth_date: datetime
    preferences: str
    location: str


# Pydantic model for user response
class UserResponse(BaseModel):
    """Pydantic model for user response"""

    id: int
    email: str
    name: str
    gender: str
    birth_date: datetime
    preferences: str
    location: str
    age: int

    class Config:
        """Only a validation class to the attributes
        """
        from_attributes = True


# Dependency to get the database session
def get_db() -> Session: # type: ignore
    """Dependency to get the database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to calculate age from birth date
def calculate_age(birth_date: datetime) -> int:
    """Calculate age from birth date"""
    return datetime.now().year - birth_date.year

