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
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.exc import IntegrityError, SQLAlchemyError 
import uvicorn
from DB import UsuarioCreate, Session, get_db, calculate_age, UserResponse # pylint: disable=E0611
from user import Usuario

# Importa las clases y funciones necesarias


# Crea una instancia de FastAPI
app = FastAPI()

# Define las rutas y funciones de la API
@app.get("/")
def read_root():
    """Route to '/' wher we can verify if the api is created.

    Returns:
        message: ....
    """
    return {"message": "Welcome to the dating app API!"}

# Otros endpoints de la API pueden ser definidos aquí
@app.post("/usuarios/")
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)): # type: ignore
    """Create a new user"""
    try:
        age = calculate_age(usuario.birth_date)
        usuario_data = usuario.dict()
        usuario_data["age"] = age
        db_usuario = Usuario(**usuario_data)
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return {"mensaje": "Usuario creado exitosamente"}
    except ValueError as ve:
        return {"error": f"ValueError: {ve}"}
    except IntegrityError as ie:
        return {"error": f"IntegrityError: {ie}"}
    except SQLAlchemyError as se:
        return {"error": f"SQLAlchemyError: {se}"}



@app.get("/usuarios/", response_model=list[UserResponse])
def read_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Retrieve a list of users"""
    usuarios = db.query(Usuario).offset(skip).limit(limit).all()
    for usuario in usuarios:
        usuario.age = calculate_age(usuario.birth_date)
    return usuarios


@app.get("/usuarios/{usuario_id}", response_model=UserResponse)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)): # type: ignore
    """Retrieve a user by ID"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.age = calculate_age(usuario.birth_date)
    return usuario

from fastapi import HTTPException

@app.put("/usuarios/{usuario_id}")
def update_usuario(usuario_id: int, usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """Update user data"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar los campos especificados
    if usuario_data.id:
        usuario.id = usuario_data.id
    if usuario_data.name:
        usuario.name = usuario_data.name
    if usuario_data.gender:
        usuario.gender = usuario_data.gender
    if usuario_data.location:
        usuario.location = usuario_data.location
    if usuario_data.preferences:
        usuario.preferences = usuario_data.preferences
    
    # Guardar los cambios en la base de datos
    db.commit()
    db.refresh(usuario)
    return {"mensaje": "Datos de usuario actualizados exitosamente"}



@app.delete("/usuarios/{usuario_id}")
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Delete a user by ID"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"mensaje": "Usuario eliminado exitosamente"}









# Inicia el servidor Uvicorn
if __name__ == "__main__":
    print("Starting Uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
