from sqlalchemy import Boolean, Column, ForeignKey, Integer, LargeBinary, String, TIMESTAMP, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import  *
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

#This code line create the tables on 'udinder' Database of postgres
Base.metadata.create_all(bind=engine)
