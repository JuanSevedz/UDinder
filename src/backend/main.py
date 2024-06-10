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
from fastapi import FastAPI, HTTPException, Depends,File, UploadFile, Form
from sqlalchemy.exc import IntegrityError, SQLAlchemyError 
import uvicorn
from database import UserCreate, Session,SessionLocal, get_db, calculate_age, UserResponse, UserUpdate # pylint: disable=E0611
from models import User, Profile
from auth import Authentication
# Import the necessary classes and functions


# Create a FastAPI instance
app = FastAPI()

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

auth = Authentication(get_db_session())

# Define the API routes and functions
@app.get("/")
def read_root():
    """Route to '/' where we can verify if the API is created.

    Returns:
        message: ....
    """
    return {"message": "Welcome to the dating app API!"}

# For User
@app.post("/users/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    auth = Authentication(db)
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
        # Crear perfil asociado al usuario
        db_profile = Profile(user_id=db_user.id)  # Aquí asumimos que el ID del usuario se genera automáticamente
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
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)): # type: ignore
    """Retrieve a list of users"""
    users = db.query(User).offset(skip).limit(limit).all()
    for user in users:
        user.age = calculate_age(user.birth_date)
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def read_specific_user(user_id: int, db: Session = Depends(get_db)): # type: ignore
    """Retrieve a user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.age = calculate_age(user.birth_date)
    return user

@app.put("/users/{user_id}", name="update_user")
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)): # type: ignore
    """Update user data"""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Actualizar los campos especificados
    update_data = user_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(user, key):  # Verificar que el campo exista en el modelo User
            setattr(user, key, value)
    
    # Guardar los cambios en la base de datos
    db.commit()
    db.refresh(user)
    return {"message": "User data updated successfully"}

@app.delete("/users/{user_id}")
def delete_account(user_id: int, db: Session = Depends(get_db)): # type: ignore
    """Delete a user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


# For Authentication 
@app.post("/login")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    auth = Authentication(db)
    user = auth.login(email, password)
    if user:
        return {"message": "User logged in successfully"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/logout")
def logout_user(db: Session = Depends(get_db)):
    auth = Authentication(db)
    auth.logout()
    return {"message": "User logged out successfully"}



# For Profile


# Endpoint para subir foto
@app.post("/profiles/upload-photo/")
def upload_photo(user_id: int, photo: UploadFile = File(...), db: Session = Depends(get_db)):
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

# Endpoint para agregar descripción
@app.put("/profiles/add-description/")
def add_description(user_id: int, description: str = Form(...), db: Session = Depends(get_db)):
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
def set_interests(user_id: int, interests: str = Form(...), db: Session = Depends(get_db)):
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



# Start the Uvicorn server
if __name__ == "__main__":
    print("Starting Uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)