from sqlalchemy.orm import Session
from models import User

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
