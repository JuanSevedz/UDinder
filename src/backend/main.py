"""
Imports for setting up a FastAPI application with SQLAlchemy database integration.

Imports:
    - FastAPI: A modern, fast (high-performance) web framework for building APIs with Python.
    - HTTPException: Exception to return as an HTTP response.
    - Depends: A decorator for dependencies.
    - BaseModel: Base class for creating Pydantic models.
    - EmailStr: Email validation string type from Pydantic.
    - create_engine: Function to create a SQLAlchemy engine.
    - Column: Class to represent a column in a database table.
    - Integer: Integer data type from SQLAlchemy.
    - String: String data type from SQLAlchemy.
    - TIMESTAMP: TIMESTAMP data type from SQLAlchemy.
    - func: Module for SQL functions in SQLAlchemy.
    - declarative_base: Function for creating a base class for declarative class definitions.
    - sessionmaker: Function for creating a session factory in SQLAlchemy.
    - Session: Represents a database session in SQLAlchemy.
    - datetime: Module for manipulating dates and times.
    - uvicorn: ASGI server implementation, used for running the FastAPI application.

Note: Ensure you have the necessary packages installed to use these imports.
"""
from typing import List

import uvicorn
from auth import *  # pylint: disable=wildcard-import, unused-wildcard-import
from database import (MessageCreate, MessageResponse,  # pylint: disable=E0611
                      Session, SessionLocal, UserCreate, UserResponse,
                      UserUpdate, calculate_age, get_db, LoginData)
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from models import Match, Message, Profile, User
from routes_admin import router as admin_router
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound


# Create a FastAPI instance
app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")


# Configuration of CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)



def get_db_session():
    """
    Get a database session.

    Returns:
        Session: A database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

auth = Authentication(get_db_session())

@app.get("/favicon.ico")
async def favicon():
    """
    Serve the favicon.ico file.

    This endpoint serves the favicon.ico file from the static/images directory.
    The favicon is a small icon that appears in the browser tab next to the site's title.

    Returns:
        FileResponse: The response containing the favicon.ico file.
    """
    return FileResponse("static/images/favicon.ico")


# Define the API routes and functions
@app.get("/", response_class=HTMLResponse)
async def index():
    """
    Get the index page.

    Returns:
        HTMLResponse: The HTML content of the index page.
    """
    with open("../frontend/templates/index.html", "r") as file: # pylint: disable=unspecified-encoding
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/api/endpoint")
async def endpoint():
    """
    Endpoint for /api/endpoint.

    Returns:
        dict: A message indicating the response from /api/endpoint.
    """
    return {"message": "This is the response from /api/endpoint"}

# For User
@app.post("/users/add")
def register_user(user: UserCreate, db: Session = Depends(get_db)): # type: ignore
    """
    Register a new user.

    Args:
        user (UserCreate): The user data to register.
        db (Session): The database session.

    Returns:
        dict: A message indicating the result of the registration process.
    """
    auth = Authentication(db) # pylint: disable=redefined-outer-name
    if auth.is_email_registered(user.email):
        raise HTTPException(status_code=400, detail="Email is already registered")
    try:
        age = calculate_age(user.birth_date)
        user_data = user.dict()
        user_data["age"] = age
        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        db_profile = Profile(user_id=db_user.id)
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return {"message": "User created successfully"}
    except ValueError as ve:
        return {"error": f"ValueError: {ve}"}
    except IntegrityError as ie:
        return {"error": f"IntegrityError: {ie}"}
    except SQLAlchemyError as se:
        return {"error": f"SQLAlchemyError: {se}"}

@app.get("/users/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)): # type: ignore
    """
    Retrieve a list of users.

    Args:
        db (Session): The database session.

    Returns:
        List[UserResponse]: A list of user objects.
    """
    users = db.query(User).all()
    for user in users:
        user.age = calculate_age(user.birth_date)
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def read_specific_user(user_id: int, db: Session = Depends(get_db)): # type: ignore
    """
    Retrieve a user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session): The database session.

    Returns:
        UserResponse: The user object.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.age = calculate_age(user.birth_date)
    return user

@app.put("/users/{user_id}", name="update_user")
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)): # type: ignore
    """
    Update user data.

    Args:
        user_id (int): The ID of the user to update.
        user_data (UserUpdate): The updated user data.
        db (Session): The database session.

    Returns:
        dict: A message indicating the result of the update operation.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(user, key): 
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return {"message": "User data updated successfully"}


# Delete User and Profile at the same time
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)): # type: ignore
    """
    Delete a user and their associated profile.

    Args:
        user_id (int): The ID of the user to delete.
        db (Session): The database session.

    Returns:
        dict: A message indicating the result of the deletion operation.
    """
    try:
        
        user = db.query(User).filter(User.id == user_id).one() # Find User
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found") # pylint: disable=raise-missing-from
    
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if profile:
        db.delete(profile)
    
    db.delete(user)
    db.commit()
    
    return {"message": "User and profile deleted successfully"}



# For Authentication 
@app.post("/login")
def login_user(login_data: LoginData, db: Session = Depends(get_db)): # type: ignore
  
    """
    Log in a user.

    Args:
        email (str): The user's email.
        password (str): The user's password.
        db (Session): The database session.

    Returns:
        dict: A message indicating the result of the login attempt.
    """
    auth = Authentication(db) # pylint: disable=redefined-outer-name
    user = auth.login(login_data.email, login_data.password)
    if user:
        return {"message": "User logged in successfully"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/logout")
def logout_user(db: Session = Depends(get_db)):  # type: ignore
    """
    Log out the current user.

    Args:
        db (Session): The database session.

    Returns:
        dict: A message indicating the result of the logout operation.
    """
    auth = Authentication(db) # pylint: disable=redefined-outer-name
    auth.logout()
    return {"message": "User logged out successfully"}



# For Profile
@app.post("/profiles/upload-photo/")
def upload_photo(user_id: int, photo: UploadFile = File(...), db: Session = Depends(get_db)): # type: ignore
    """
    Upload a photo for a user profile.

    Args:
        user_id (int): The ID of the user.
        photo (UploadFile): The photo file to upload.
        db (Session): The database session.

    Returns:
        dict: A message indicating the result of the photo upload.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    photo_content = photo.file.read()
    profile.photo = photo_content
    db.commit()
    db.refresh(profile)
    return {"message": "Photo uploaded successfully"}

@app.put("/profiles/add-description/")
def add_description(user_id: int, description: str = Form(...), db: Session = Depends(get_db)): # type: ignore
    """
    Add a description to a user's profile.

    Args:
        user_id (int): The ID of the user.
        description (str): The description to add.
        db (Session): The database session.

    Returns:
        dict: A message indicating the result of adding the description.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    profile.description = description
    db.commit()
    db.refresh(profile)
    return {"message": "Description added successfully"}

# Endpoint para colocar intereses
@app.put("/profiles/set-interests/")
def set_interests(user_id: int, interests: str = Form(...), db: Session = Depends(get_db)): # type: ignore
    """
    Set interests for a user's profile.

    Args:
        user_id (int): The ID of the user.
        interests (str): The interests to set.
        db (Session): The database session.

    Returns:
        dict: A message indicating the result of setting the interests.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    profile.interests = interests
    db.commit()
    db.refresh(profile)
    return {"message": "Interests set successfully"}




# route for admin
app.include_router(admin_router)


# Matches Endpoints
@app.post("/like/{user_id}/{liked_user_id}")
def like_user(user_id: int, liked_user_id: int, db: Session = Depends(get_db)): # type: ignore
    """
    Like a user.

    Args:
        user_id (int): The ID of the user giving the like.
        liked_user_id (int): The ID of the user being liked.
        db (Session): The database session.

    Returns:
        dict: A message indicating the result of the like action.
    """
    if user_id == liked_user_id:
        raise HTTPException(status_code=400, detail="Users cannot like themselves")
    
    # Verify an existing like or not
    match = db.query(Match).filter(Match.user_id == user_id, Match.liked_user_id == liked_user_id).first()
    if match:
        raise HTTPException(status_code=400, detail="Like already exists")
    
    # Make the"like"
    new_like = Match(user_id=user_id, liked_user_id=liked_user_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    
    reciprocal_match = db.query(Match).filter(Match.user_id == liked_user_id, Match.liked_user_id == user_id).first()
    if reciprocal_match:
        return {"message": "It's a match!"}
    
    return {"message": "Like registered"}



@app.get("/matches/{user_id}", response_model=List[UserResponse])
def get_matches(user_id: int, db: Session = Depends(get_db)): # type: ignore
    """
    Get matches for a user.

    Args:
        user_id (int): The ID of the user.
        db (Session): The database session.

    Returns:
        List[UserResponse]: A list of matched users.
    """
    matches = db.query(Match).filter(
        Match.user_id == user_id
    ).all()

    match_user_ids = set()
    for match in matches:
        reciprocal_match = db.query(Match).filter(Match.user_id == match.liked_user_id, Match.liked_user_id == user_id).first()
        if reciprocal_match:
            match_user_ids.add(match.liked_user_id)
    
    matched_users = db.query(User).filter(User.id.in_(match_user_ids)).all()
    
    matched_users_response = [UserResponse.from_orm(user) for user in matched_users]
    
    return matched_users_response


# Endpoint for Admin delete matches
@app.delete("/matches/{match_id}")
def delete_match(match_id: int, db: Session = Depends(get_db)): # type: ignore
    """
    Delete a match.

    Args:
        match_id (int): The ID of the match to delete.
        db (Session): The database session.

    Returns:
        dict: A message indicating the result of the deletion operation.
    """
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    db.delete(match)
    db.commit()
    return {"message": "Match deleted successfully"}

# Functions to send and recive messages

def create_message(db: Session, message: MessageCreate): # type: ignore
    """
    Create a new message.

    Args:
        db (Session): The database session.
        message (MessageCreate): The message data.

    Returns:
        Message: The created message.
    """
    db_message = Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_user_messages(db: Session, user_id: str): # type: ignore
    """
    Get messages for a user.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user.

    Returns:
        List[Message]: A list of messages for the user.
    """
    return db.query(Message).filter(Message.receiver_id == user_id).all()


@app.post("/messages/", response_model=MessageResponse)
def send_message(message: MessageCreate, db: Session = Depends(get_db)): # type: ignore
    """
    Send a message.

    Args:
        message (MessageCreate): The message data.
        db (Session): The database session.

    Returns:
        MessageResponse: The created message.
    """
    receiver = db.query(User).filter(User.id == message.receiver_id).first()
    if receiver is None:
        raise HTTPException(status_code=404, detail="The receiving user does not exist")

    # Is the same user
    if message.sender_id == message.receiver_id:
        raise HTTPException(status_code=400, detail="You can't send a message to yourself")

    match = db.query(Match).filter(
        ((Match.user_id == message.sender_id) & (Match.liked_user_id == message.receiver_id)) |
        ((Match.user_id == message.receiver_id) & (Match.liked_user_id == message.sender_id))
    ).first()
    if not match:
        raise HTTPException(status_code=400, detail="There is no match between the sender and the receiver")

    return create_message(db=db, message=message)


@app.get("/messages/{user_id}/", response_model=list[MessageResponse])
def get_user_messages_endpoint(user_id: str, db: Session = Depends(get_db)): # type: ignore
    """
    Get messages for a user.

    Args:
        user_id (str): The ID of the user.
        db (Session): The database session.

    Returns:
        List[MessageResponse]: A list of messages for the user.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    
    messages = get_user_messages(db, user_id=user_id)
    return messages


@app.delete("/messages/{message_id}/", response_model=None)
def delete_message(message_id: int, db: Session = Depends(get_db)): # type: ignore
    """
    Delete a message.

    Args:
        message_id (int): The ID of the message to delete.
        db (Session): The database session.

    Returns:
        None: Indicates successful deletion.
    """
    message = db.query(Message).filter(Message.id == message_id).first()

    if not message:
        raise HTTPException(status_code=404, detail="The message was not found")

    db.delete(message)
    db.commit()
    
    return message




# Start the Uvicorn server
if __name__ == "__main__":
    print("Starting Uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)