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
from fastapi import FastAPI, HTTPException, Depends,File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound 
import uvicorn
from database import UserCreate, Session,SessionLocal, get_db, calculate_age, UserResponse, UserUpdate # pylint: disable=E0611
from fastapi.middleware.cors import CORSMiddleware
from models import User, Profile, Match, Message
from routes_admin import router as admin_router
from auth import * # pylint: disable=W0401

# Import the necessary classes and functions


# Create a FastAPI instance
app = FastAPI()

# Montar las carpetas de archivos estáticos como rutas estáticas en tu aplicación FastAPI
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Esto permitirá todas las solicitudes de cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Esto permitirá todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Esto permitirá todos los encabezados en las solicitudes
)



def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

auth = Authentication(get_db_session())

# Define the API routes and functions
@app.get("/", response_class=HTMLResponse)
async def index():
    # Leer el archivo HTML y servirlo como respuesta HTML
    with open("../frontend/templates/index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/api/endpoint")
async def endpoint():
    return {"message": "This is the response from /api/endpoint"}




# For User
@app.post("/users/add")
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
def read_users(db: Session = Depends(get_db)): # type: ignore
    """Retrieve a list of users"""
    users = db.query(User).all()
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


# Delete User and Profile at the same time
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        # Buscar el usuario
        user = db.query(User).filter(User.id == user_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Eliminar el perfil asociado
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if profile:
        db.delete(profile)
    
    # Eliminar el usuario
    db.delete(user)
    db.commit()
    
    return {"message": "User and profile deleted successfully"}



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




# route for admin
app.include_router(admin_router)


# Matches Endpoints
@app.post("/like/{user_id}/{liked_user_id}")
def like_user(user_id: int, liked_user_id: int, db: Session = Depends(get_db)): # type: ignore
    if user_id == liked_user_id:
        raise HTTPException(status_code=400, detail="Users cannot like themselves")
    
    # Verificar si ya existe el "like"
    match = db.query(Match).filter(Match.user_id == user_id, Match.liked_user_id == liked_user_id).first()
    if match:
        raise HTTPException(status_code=400, detail="Like already exists")
    
    # Crear el "like"
    new_like = Match(user_id=user_id, liked_user_id=liked_user_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)

    # Verificar si el otro usuario también ha indicado que le gusta (es un "match")
    reciprocal_match = db.query(Match).filter(Match.user_id == liked_user_id, Match.liked_user_id == user_id).first()
    if reciprocal_match:
        return {"message": "It's a match!"}
    
    return {"message": "Like registered"}



@app.get("/matches/{user_id}", response_model=List[UserResponse])
def get_matches(user_id: int, db: Session = Depends(get_db)):
    # Obtener los "matches" donde hay reciprocidad
    matches = db.query(Match).filter(
        Match.user_id == user_id
    ).all()

    match_user_ids = set()
    for match in matches:
        reciprocal_match = db.query(Match).filter(Match.user_id == match.liked_user_id, Match.liked_user_id == user_id).first()
        if reciprocal_match:
            match_user_ids.add(match.liked_user_id)
    
    # Obtener los detalles de los usuarios con los que hay "match" mutuo
    matched_users = db.query(User).filter(User.id.in_(match_user_ids)).all()
    
    # Convertir los objetos User a UserResponse
    matched_users_response = [UserResponse.from_orm(user) for user in matched_users]
    
    return matched_users_response


# Endpoint for Admin delete matches
@app.delete("/matches/{match_id}")
def delete_match(match_id: int, db: Session = Depends(get_db)): # type: ignore
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    db.delete(match)
    db.commit()
    return {"message": "Match deleted successfully"}

# Functions to send and recive messages

def create_message(db: Session, message: MessageCreate):
    # Crea un nuevo mensaje en la base de datos
    db_message = Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_user_messages(db: Session, user_id: str):
    # Obtiene los mensajes de un usuario de la base de datos
    return db.query(Message).filter(Message.receiver_id == user_id).all()


# Endpoint para enviar un mensaje
# Endpoint para enviar un mensaje
@app.post("/messages/", response_model=MessageResponse)
def send_message(message: MessageCreate, db: Session = Depends(get_db)):
    # Comprobar si el usuario receptor existe
    receiver = db.query(User).filter(User.id == message.receiver_id).first()
    if receiver is None:
        raise HTTPException(status_code=404, detail="El usuario receptor no existe")

    # Verificar si el remitente y el receptor son el mismo usuario
    if message.sender_id == message.receiver_id:
        raise HTTPException(status_code=400, detail="No puedes enviar un mensaje a ti mismo")

    # Verificar si existe un match entre el remitente y el receptor
    match = db.query(Match).filter(
        ((Match.user_id == message.sender_id) & (Match.liked_user_id == message.receiver_id)) |
        ((Match.user_id == message.receiver_id) & (Match.liked_user_id == message.sender_id))
    ).first()
    if not match:
        raise HTTPException(status_code=400, detail="No hay match entre el remitente y el receptor")

    # Si el usuario receptor existe y hay un match, crear el mensaje en la base de datos
    return create_message(db=db, message=message)

# Endpoint para obtener los mensajes de un usuario
@app.get("/messages/{user_id}/", response_model=list[MessageResponse])
def get_user_messages_endpoint(user_id: str, db: Session = Depends(get_db)):
    # Comprobar si el usuario existe
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    # Obtener los mensajes del usuario
    messages = get_user_messages(db, user_id=user_id)
    return messages


# Endpoint para borrar un mensaje
@app.delete("/messages/{message_id}/", response_model=None)
def delete_message(message_id: int, db: Session = Depends(get_db)):
    # Buscar el mensaje en la base de datos
    message = db.query(Message).filter(Message.id == message_id).first()

    # Si el mensaje no existe, levantar una excepción HTTP 404
    if not message:
        raise HTTPException(status_code=404, detail="El mensaje no fue encontrado")

    # Borrar el mensaje de la base de datos
    db.delete(message)
    db.commit()
    
    return message




# Start the Uvicorn server
if __name__ == "__main__":
    print("Starting Uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)