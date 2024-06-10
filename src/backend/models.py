from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
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

Base.metadata.create_all(bind=engine)
