"""
This module contains the necessary imports for defining and managing database models using SQLAlchemy ORM (Object Relational Mapping). It includes various SQLAlchemy components for defining columns, data types, relationships, and constraints in a declarative manner.

Imports:
    from sqlalchemy import Boolean, Column, ForeignKey, Integer, LargeBinary, String, TIMESTAMP, Text, UniqueConstraint
        - Provides various column types and constraints that can be used in table definitions.
        
        - Boolean: A column type that stores True/False values.
        - Column: A generic column in a table, used to define attributes of the table.
        - ForeignKey: Defines a column that is a foreign key to another table.
        - Integer: A column type for integer values.
        - LargeBinary: A column type for large binary data, such as files or images.
        - String: A column type for string data.
        - TIMESTAMP: A column type for timestamp data, including both date and time.
        - Text: A column type for large text data.
        - UniqueConstraint: Defines a unique constraint for one or more columns in a table.
        
    from sqlalchemy.ext.declarative import declarative_base
        - Used to create a base class for declarative class definitions. This base class keeps track of all tables and mappers defined by subclasses.
        
    from sqlalchemy.orm import relationship
        - Used to define relationships between different tables/models. It allows for easy access and manipulation of related data.

Usage:
    These imports are typically used in combination to define database models (tables) in a Pythonic way. Below is an example of how they might be used:

    ```python
    from sqlalchemy import Boolean, Column, ForeignKey, Integer, LargeBinary, String, TIMESTAMP, Text, UniqueConstraint
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'users'
        
        id = Column(Integer, primary_key=True)
        username = Column(String, unique=True, nullable=False)
        email = Column(String, unique=True, nullable=False)
        hashed_password = Column(String, nullable=False)
        is_active = Column(Boolean, default=True)
        created_at = Column(TIMESTAMP, nullable=False)
        
        posts = relationship('Post', back_populates='author')

    class Post(Base):
        __tablename__ = 'posts'
        
        id = Column(Integer, primary_key=True)
        title = Column(String, nullable=False)
        content = Column(Text, nullable=False)
        author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
        created_at = Column(TIMESTAMP, nullable=False)
        
        author = relationship('User', back_populates='posts')

        __table_args__ = (
            UniqueConstraint('title', name='unique_post_title'),
        )
    ```
    
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, LargeBinary, String, TIMESTAMP, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import  * # pylint: disable=wildcard-import, unused-wildcard-import
Base = declarative_base()


class User(Base):
    """Database model for user"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=False)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    gender = Column(String)
    birth_date = Column(TIMESTAMP)
    preferences = Column(String)
    location = Column(String)
    age = Column(Integer)
    
    # Define la relación con el perfil
    admin = relationship("Admin", back_populates="user")
    profile = relationship("Profile", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    photo = Column(LargeBinary, nullable=True)
    description = Column(Text, nullable=True)
    interests = Column(Text, nullable=True)
    
    # Define la relación con el usuario
    user = relationship("User", back_populates="profile")
    

class Admin(Base):
    """Database model for admin"""

    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    is_blocked = Column(Boolean, default=False)

    user = relationship("User", back_populates="admin")

class Match(Base):
    """Datase model for match history"""
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    liked_user_id = Column(Integer, ForeignKey('users.id'))
    
    __table_args__ = (UniqueConstraint('user_id', 'liked_user_id', name='unique_match'),)

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    message = Column(String)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])

#This code line create the tables on 'udinder' Database of postgres
Base.metadata.create_all(bind=engine)
