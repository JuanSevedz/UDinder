"""
Endpoints for managing admin users.

Includes routes for creating admins, blocking and unblocking users by their user ID.

Routes:
- POST /admin/create-admin/{user_id}: Creates a new admin user associated with the given user ID.
- PUT /admin/block-user/{user_id}: Blocks a user by their user ID. Requires authentication as an admin.
- PUT /admin/unblock-user/{user_id}: Unblocks a user by their user ID. Requires authentication as an admin.

Parameters:
- user_id (int): The ID of the user to perform actions on.

Dependencies:
- db (Session): SQLAlchemy database session.
- current_admin (Admin): The current authenticated admin user. Required for routes that modify admin status.

Returns:
- JSON response indicating success or failure of the operation.

Exceptions:
- HTTPException: Raises HTTPException with appropriate status code and details if any error occurs during the operation.
"""

from sqlalchemy import Boolean, ForeignKey, Column, Integer #pylint: disable=unused-import
from sqlalchemy.orm import relationship #pylint: disable=unused-import
from database import * #pylint: disable=W0614
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Admin
from database import get_db
from auth import get_current_admin,get_current_user,create_access_token,is_admin #pylint: disable=unused-import


router = APIRouter()

@router.post("/admin/create-admin/{user_id}")
def create_admin(user_id: int, db: Session = Depends(get_db)): # type:ignore
    """
Create a new admin user associated with the given user ID.

Parameters:
- user_id (int): The ID of the user to be promoted as an admin.

Dependencies:
- db (Session): SQLAlchemy database session.

Returns:
- JSON response indicating success or failure of the operation.

Exceptions:
- HTTPException: Raises HTTPException with status code 400 if the user is already an admin.
"""

    existing_admin = db.query(Admin).filter(Admin.user_id == user_id).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="User is already an admin")
    
    
    admin = Admin(user_id=user_id)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return {"message": "Admin created successfully"}

@router.put("/admin/block-user/{user_id}")
def block_user(user_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)): # type:ignore
    """
Block a user by their user ID.

This action requires authentication as an admin.

Parameters:
- user_id (int): The ID of the user to be blocked.

Dependencies:
- db (Session): SQLAlchemy database session.
- current_admin (Admin): The current authenticated admin user.

Returns:
- JSON response indicating success or failure of the operation.

Exceptions:
- HTTPException: Raises HTTPException with status code 401 if authentication fails, or 404 if the admin entry is not found.
"""

    
    if current_admin is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    
    admin_entry = db.query(Admin).filter(Admin.user_id == user_id).first()
    if admin_entry is None:
        raise HTTPException(status_code=404, detail="Admin entry not found")

    
    admin_entry.is_blocked = True
    db.commit()
    return {"message": "User blocked successfully"}


@router.put("/admin/unblock-user/{user_id}")
def unblock_user(user_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)): # type:ignore
    """
Unblock a user by their user ID.

This action requires authentication as an admin.

Parameters:
- user_id (int): The ID of the user to be unblocked.

Dependencies:
- db (Session): SQLAlchemy database session.
- current_admin (Admin): The current authenticated admin user.

Returns:
- JSON response indicating success or failure of the operation.

Exceptions:
- HTTPException: Raises HTTPException with status code 401 if authentication fails, or 404 if the admin entry is not found.
"""

    if current_admin is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    
    admin_entry = db.query(Admin).filter(Admin.user_id == user_id).first()
    if admin_entry is None:
        raise HTTPException(status_code=404, detail="Admin entry not found")

    
    admin_entry.is_blocked = False
    db.commit()
    return {"message": "User unblocked successfully"}
