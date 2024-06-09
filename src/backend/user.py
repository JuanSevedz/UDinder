from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from DB import *
Base = declarative_base()

class Usuario(Base):
    """Modelo de base de datos para usuario"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    gender = Column(String)
    birth_date = Column(TIMESTAMP)
    preferences = Column(String)
    location = Column(String)
    age = Column(Integer)
