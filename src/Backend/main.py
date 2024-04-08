from db_connection import test_function,DBConnection
from application_servers import *

def main():
    print("Welcome to the registration program!")
    if check_registration():
        print("You are already registered.")
        # Agrega aquí cualquier otra lógica que desees ejecutar si el usuario está registrado
    else:
        print("You are not registered yet.")
        user_sign_up()

    # Luego puedes continuar con otras partes de tu programa según sea necesario

if __name__ == "__main__":
    main()
connection = DBConnection()
connection.connect()

test_function()

