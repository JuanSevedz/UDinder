"""
This module includes the necessary imports for working with datetime operations,
OS operations, Pydantic models, SQLAlchemy ORM, and type hinting.

Imports:
    from datetime import datetime:
        Provides classes for manipulating dates and times.
        
    import os:
        Provides a portable way of using operating system dependent functionality like reading or writing to the file system.
        
    from pydantic import BaseModel, EmailStr:
        BaseModel: The base class for creating Pydantic models, which offer data validation and parsing.
        EmailStr: A custom type for email strings, ensuring valid email formats.
        
    from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func:
        create_engine: A factory function for creating a new SQLAlchemy engine instance.
        Column: A class for defining columns in SQLAlchemy models.
        Integer: A class for defining integer columns in SQLAlchemy models.
        String: A class for defining string columns in SQLAlchemy models.
        TIMESTAMP: A class for defining timestamp columns in SQLAlchemy models.
        func: A module that provides access to SQL functions like `now()`.
        
    from sqlalchemy.orm import declarative_base, sessionmaker, Session:
        declarative_base: A factory function for creating a base class for declarative class definitions.
        sessionmaker: A factory for creating new SQLAlchemy session objects.
        Session: A class for creating SQLAlchemy session instances.
        
    from typing import Optional:
        Optional: A utility for indicating that a variable can be of a specified type or None.
"""
from datetime import datetime
import os
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func # pylint: disable=unused-import
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import Session
from typing import Optional

# Define the database URL using environment variables
DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_URL')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Create the engine for the database connection
engine = create_engine(DATABASE_URL)

# Create a session local to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a session instance
Session = SessionLocal()

# Create a base class for declarative class definitions
Base = declarative_base()

# Create tables in the database
print("Creating tables in the database...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")




class UserCreate(BaseModel):
    """
    Pydantic model for creating a new user.

    Attributes:
        id (int): The unique identifier for the user.
        email (EmailStr): The email address of the user.
        name (str): The name of the user.
        password (str): The password of the user.
        gender (str, optional): The gender of the user (optional).
        birth_date (datetime, optional): The birth date of the user (optional).
        preferences (str, optional): The preferences of the user (optional).
        location (str, optional): The location of the user (optional).
        age (int, optional): The age of the user (optional).
    """
    id: int
    email: EmailStr
    name: str
    password: str
    gender: Optional[str]
    birth_date: Optional[datetime]
    preferences: Optional[str]
    location: Optional[str]
    age: Optional[int]


class UserResponse(BaseModel):
    """
    Represents the response structure for a user.

    Attributes:
        id (int): The unique ID of the user.
        email (EmailStr): The email address of the user.
        name (str): The name of the user.
        gender (Optional[str]): The gender of the user. Optional.
        birth_date (Optional[datetime]): The birth date of the user. Optional.
        preferences (Optional[str]): The preferences of the user. Optional.
        location (Optional[str]): The location of the user. Optional.
        age (Optional[int]): The age of the user. Optional.
        
    Config:
        from_attributes (bool): If True, populate model from attributes (default: False).
    """
    id: int
    email: EmailStr
    name: str
    gender: Optional[str]
    birth_date: Optional[datetime]
    preferences: Optional[str]
    location: Optional[str]
    age: Optional[int]
    
    class Config:
        """Configuration for the validation of attributes."""
        from_attributes = True

class UserUpdate(BaseModel):
    """
    Represents a model for updating an existing user.

    Attributes:
        name (Optional[str]): The updated name of the user. Optional.
        password (Optional[str]): The updated password of the user. Optional.
        preferences (Optional[str]): The updated preferences of the user. Optional.
        location (Optional[str]): The updated location of the user. Optional.
    """
    name: Optional[str] = None
    password: Optional[str] = None
    preferences: Optional[str] = None
    location: Optional[str] = None

class MessageCreate(BaseModel):
    """
    Represents the structure of a message to be created.
    
    Attributes:
        sender_id (int): The ID of the sender of the message.
        receiver_id (int): The ID of the receiver of the message.
        message (str): The content of the message.
    """
    sender_id: int
    receiver_id: int
    message: str

class MessageResponse(BaseModel):
    """
    Represents the structure of a message response.
    
    Attributes:
        id (int): The unique ID of the message.
        sender_id (int): The ID of the sender of the message.
        receiver_id (int): The ID of the receiver of the message.
        message (str): The content of the message.
    
    Config:
        from_attributes (bool): If True, populate model from attributes (default: False).
    """
    id: int
    sender_id: int
    receiver_id: int
    message: str

    class Config:
        from_attributes = True

class LoginData(BaseModel):
    email: str
    password: str

def get_db() -> Session: # type: ignore
    """
    Dependency to get the database session.

    Yields:
        Session: A SQLAlchemy database session.
    
    This function is used to provide a database session for the duration of a request.
    It ensures that the session is properly closed after the request is processed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def calculate_age(birth_date: datetime) -> int:
    """
    Calculate age from birth date.

    Args:
        birth_date (datetime): The birth date of the individual.

    Returns:
        int: The age of the individual based on the current date.
    
    This function calculates the age by comparing the birth date with the current date.
    It takes into account whether the current date has already passed the birthday for the current year.
    """
    today = datetime.now()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))