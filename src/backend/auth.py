from datetime import timedelta, datetime
import token
from sqlalchemy.orm import Session
from models import Admin, User
from database import get_db
from typing import Optional
import jwt
from jwt import PyJWTError
from fastapi import Depends, HTTPException, Header



class Authentication:
    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, email: str, password: str):
        return self.db.query(User).filter(User.email == email, User.password == password).first()

    def login(self, email: str, password: str):
        user = self.authenticate_user(email, password)
        if user:
            print("Inicio de sesión exitoso.")
            return user
        else:
            print("Credenciales inválidas.")
            return None

    def logout(self):
        print("Sesión cerrada.")

    def is_email_registered(self, email: str):
        return self.db.query(User).filter(User.email == email).first() is not None
    
    
    
# Admin
SECRET_KEY = "hola"  # Clave secreta para firmar los tokens
ALGORITHM = "HS256"  # Algoritmo de encriptación para los tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tiempo de expiración del token en minutos



def get_current_user(token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




def is_admin(username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    # Verificar si el usuario es administrador
    if not is_admin(username, db):
        raise HTTPException(status_code=403, detail="User is not an admin")
    return username

def get_current_admin(token: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        if token is None:
            raise HTTPException(status_code=401, detail="Token is missing")
        
        # Decodificar el token para obtener la información del administrador
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        
        # Verificar si el usuario asociado al token es un administrador
        admin_id = payload.get("sub")
        admin = db.query(Admin).filter(Admin.id == admin_id).first()
        if admin is None:
            raise HTTPException(status_code=401, detail="User is not an admin")
        
        return admin
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


