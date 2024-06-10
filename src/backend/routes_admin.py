from sqlalchemy import Boolean, ForeignKey, Column, Integer, Boolean
from sqlalchemy.orm import relationship
from database import *
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Admin
from database import get_db
from auth import get_current_admin,get_current_user,create_access_token,is_admin


router = APIRouter()

@router.post("/admin/create-admin/{user_id}")
def create_admin(user_id: int, db: Session = Depends(get_db)):
    # Verificar si el usuario ya es un administrador
    existing_admin = db.query(Admin).filter(Admin.user_id == user_id).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="User is already an admin")
    
    # Crear un objeto Admin asociado al usuario
    admin = Admin(user_id=user_id)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return {"message": "Admin created successfully"}
# Bloquear usuario
@router.put("/admin/block-user/{user_id}")
def block_user(user_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    # Verificar si el usuario es administrador
    if current_admin is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Buscar el objeto Admin asociado al usuario
    admin_entry = db.query(Admin).filter(Admin.user_id == user_id).first()
    if admin_entry is None:
        raise HTTPException(status_code=404, detail="Admin entry not found")

    # Bloquear al usuario
    admin_entry.is_blocked = True
    db.commit()
    return {"message": "User blocked successfully"}

# Desbloquear usuario
@router.put("/admin/unblock-user/{user_id}")
def unblock_user(user_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    # Verificar si el usuario es administrador
    if current_admin is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Buscar el objeto Admin asociado al usuario
    admin_entry = db.query(Admin).filter(Admin.user_id == user_id).first()
    if admin_entry is None:
        raise HTTPException(status_code=404, detail="Admin entry not found")

    # Desbloquear al usuario
    admin_entry.is_blocked = False
    db.commit()
    return {"message": "User unblocked successfully"}
