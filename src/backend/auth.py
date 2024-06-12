"""
This module includes the necessary imports for working with datetime operations,
tokens, SQLAlchemy ORM, database connections, PyJWT, exceptions, and FastAPI.

Imports:
    from datetime import timedelta, datetime:
        Provides classes for manipulating dates and times.

    import token:
        Provides functions for working with tokens.

    from sqlalchemy.orm import Session:
        Provides tools for interacting with the SQLAlchemy ORM.

    from models import Admin, User:
        Imports the Admin and User models for database interactions.

    from database import get_db:
        Imports the function for getting the database session.

    from typing import Optional:
        Provides support for specifying optional types.

    import jwt:
        Provides support for JSON Web Tokens (JWT).

    from jwt import PyJWTError:
        Imports the PyJWTError class for JWT-related exceptions.

    from fastapi import Depends, HTTPException, Header:
        Imports classes and functions from FastAPI for creating web APIs.
"""
from datetime import timedelta, datetime
import token  # pylint: disable=unused-import
from sqlalchemy.orm import Session
from models import Admin, User
from database import get_db
from typing import Optional
import jwt
from jwt import PyJWTError
from fastapi import Depends, HTTPException, Header



class Authentication:
    """
    Class for handling user authentication.

    Methods:
        authenticate_user(email: str, password: str) -> User:
            Authenticates a user based on email and password.
        
        login(email: str, password: str) -> Optional[User]:
            Logs in a user based on email and password.
        
        logout():
            Logs out the current user.
        
        is_email_registered(email: str) -> bool:
            Checks if the provided email is registered in the database.
    """
    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, email: str, password: str):
        """
        Authenticates a user based on email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.

        Returns:
            User: The authenticated user object if authentication is successful.
        """
        return self.db.query(User).filter(User.email == email, User.password == password).first()

    def login(self, email: str, password: str):
        """
        Logs in a user based on email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.

        Returns:
            Optional[User]: The authenticated user object if login is successful, else None.
        """
        user = self.authenticate_user(email, password)
        if user:
            print("Inicio de sesión exitoso.")
            return user
        else:
            print("Credenciales inválidas.")
            return None

    def logout(self):
        """
        Logs out the current user.
        """
        print("Sesión cerrada.")

    def is_email_registered(self, email: str):
        """
        Checks if the provided email is registered in the database.

        Args:
            email (str): The email address to check.

        Returns:
            bool: True if the email is registered, False otherwise.
        """
        return self.db.query(User).filter(User.email == email).first() is not None
    
    
SECRET_KEY = "hola"  # Key for Admins Tokens
ALGORITHM = "HS256"  # Algorithm for encriptation of tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Time to expire for tokens



def get_current_user(token: str = Header(...)): # pylint: disable=redefined-outer-name
    """
    Obtains the current user from the provided JWT token.

    Args:
        token (str): The JWT token obtained from the request header.

    Returns:
        str: The username extracted from the token.

    Raises:
        HTTPException: If the token is missing or invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token") # pylint: disable=raise-missing-from
    
def create_access_token(data: dict, expires_delta: timedelta):
    """
    Creates a new JWT access token with the provided data.

    Args:
        data (dict): The payload data to be encoded in the token.
        expires_delta (timedelta): The duration until the token expires.

    Returns:
        str: The generated JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




def is_admin(username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Checks if the current user is an admin.

    Args:
        username (str): The username extracted from the JWT token.
        db (Session): The database session.

    Returns:
        str: The username if the user is an admin.

    Raises:
        HTTPException: If the user is not an admin.
    """
    # Verify if is User or Admin
    if not is_admin(username, db):
        raise HTTPException(status_code=403, detail="User is not an admin")
    return username

def get_current_admin(token: Optional[str] = None, db: Session = Depends(get_db)): # pylint: disable=redefined-outer-name
    """
    Obtains the current admin from the provided JWT token.

    Args:
        token (Optional[str]): The JWT token obtained from the request header.
        db (Session): The database session.

    Returns:
        Admin: The admin object extracted from the token.

    Raises:
        HTTPException: If the token is missing or invalid, or if the user is not an admin.
    """
    try:
        if token is None:
            raise HTTPException(status_code=401, detail="Token is missing")
        
        
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        
        
        admin_id = payload.get("sub")
        admin = db.query(Admin).filter(Admin.id == admin_id).first()
        if admin is None:
            raise HTTPException(status_code=401, detail="User is not an admin")
        
        return admin
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token") # pylint: disable=raise-missing-from


