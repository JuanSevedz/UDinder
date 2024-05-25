"""Module that uses the sqlite3 and hashlib libraries.

This module provides functions to interact with a SQLite database using sqlite3,
and to perform hashing operations using hashlib.
"""

import sqlite3
import hashlib


def iniciar_sesion(username_date, password_date):
    """Attempt to authenticate a user and start a session.

    This function tries to authenticate a user using their username and password.

    Args:
        username (str): The username of the user attempting to log in.
        password (str): The password provided by the user to log in.

    Returns:
        bool: True if the login is successful, False otherwise.
    """

    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()

    try:
        # Get the password hash from the database.
        c.execute(
            """SELECT password FROM usuarios WHERE username = ?""", (username_date,)
        )
        result = c.fetchone()

        if result:
            # Hash the password provided by the user.

            password_hash = hashlib.sha256(password_date.encode("utf-8")).hexdigest()

            # Compare the resulting hash with the hash stored in the database
            if password_hash == result[0]:
                print("\n¡Inicio de sesión exitoso!")
                return True
            else:
                print("¡Contraseña incorrecta!")
        else:
            print("Usuario no encontrado")

    except IOError as e:
        print("Ocurrió un error:", e)

    finally:
        conn.close()

    return False


def registrar_usuario():
    """Register a new user.

    This function prompts the user to enter a username, email, and password to register a new account.
    It then checks if the username is already in use and if the email is valid. If not, it raises
    appropriate ValueError exceptions. If registration is successful, the user's data is inserted
    into the 'usuarios' table in the database.

    Raises:
        ValueError: If the username is already in use, if the email is invalid, or if the password is empty.
        IOError: If an I/O error occurs during the process.

    """
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()

    registro_exitoso = False
    while not registro_exitoso:
        try:
            # Prompt the user to enter a username
            username_date = input("Ingrese su nombre de usuario: ")

            # Check if the username is already in use
            c.execute("""SELECT * FROM usuarios WHERE username = ?""", (username_date,))
            usuario_existente = c.fetchone()
            if usuario_existente:
                raise ValueError(
                    "El nombre de usuario ya está en uso. Por favor, elija otro."
                )

            email = input("Ingrese su correo electrónico: ")
            if "@" not in email or "." not in email:
                raise ValueError("El correo electrónico ingresado no es válido.")

            password_date = input("Ingrese su contraseña: ")
            if not password_date:
                raise ValueError("La contraseña no puede estar vacía.")

            # Hash the password before saving it to the database
            password_hash = hashlib.sha256(password_date.encode("utf-8")).hexdigest()

            # Insert the user's data into the 'usuarios' table
            c.execute(
                """INSERT INTO usuarios (username, email, password)
                         VALUES (?, ?, ?)""",
                (username_date, email, password_hash),
            )

            print("¡Usuario registrado exitosamente!")
            registro_exitoso = True

        except ValueError as ve:
            print("Error:", ve)
            print("Por favor, vuelva a intentar el proceso de registro.")

        except IOError as e:
            print("Ocurrió un error:", e)

    # Confirm changes and close the connection
    conn.commit()
    conn.close()


def mostrar_menu(username_date):
    """Display the menu options after successful login.

    This function continuously displays a menu of options to the user after they have logged in.
    The options include making swipes, viewing chats (matches), viewing profile, and logging out.
    It prompts the user to select an option and performs the corresponding action.

    Args:
        username_date (str): The username of the logged-in user.

    """
    while True:
        print("\n", f"¡Bienvenido {username_date}!")
        print("\nSeleccione una opción:")
        print("1. Hacer swipes")
        print("2. Ver chats (matches)")
        print("3. Ver perfil")
        print("4. Cerrar sesión")

        opcion_d = input("Ingrese el número de la opción deseada: ")

        if opcion_d == "1":
            print("¡Hacer swipes!")
        elif opcion_d == "2":
            print("¡Ver chats (matches)!")
        elif opcion_d == "3":
            print("¡Ver perfil!")
        elif opcion_d == "4":
            print("¡Cerrando sesión!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del 1 al 4.")

# Main
if __name__ == "__main__":
    while True:
        print("\nBienvenido a UDinder.")

        opcion = input("\n¿Desea [r]egistrarse o [i]niciar sesión? ").lower()

        if opcion == "r":
            registrar_usuario()
        elif opcion == "i":
            username = input("Ingrese su nombre de usuario: ")
            password = input("Ingrese su contraseña: ")
            if iniciar_sesion(username, password):
                mostrar_menu(username)
        else:
            print(
                "Opción no válida. Por favor, seleccione 'r' para registrarse o 'i' para iniciar sesión."
            )
