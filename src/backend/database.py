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
from typing import Optional


DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_URL')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = SessionLocal()
Base = declarative_base()

# Create tables in the database
print("Creating tables in the database...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")



# Clase Pydantic para la creación de un usuario
class UserCreate(BaseModel):
    id: int
    email: EmailStr
    name: str
    password: str
    gender: Optional[str]
    birth_date: Optional[datetime]
    preferences: Optional[str]
    location: Optional[str]
    age: Optional[int]

# Clase Pydantic para la respuesta de un usuario
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    gender: Optional[str]
    birth_date: Optional[datetime]
    preferences: Optional[str]
    location: Optional[str]
    age: Optional[int]
    
    class Config:
        """Only a validation class to the attributes
        """
        from_attributes = True

class UserUpdate(BaseModel):
    """Pydantic model for updating an existing user"""
    name: Optional[str] = None
    password: Optional[str] = None
    preferences: Optional[str] = None
    location: Optional[str] = None


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
    today = datetime.now()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
