"""This module shows the data from the SQLite database.

This module connects to the SQLite database created in DB.py and retrieves
the data from the 'usuarios' table. It then prints the retrieved data.

"""

import sqlite3

def show_database():
    """Show data from the SQLite database.

    This function connects to the 'usuarios.db' SQLite database, executes
    a SELECT query to retrieve all records from the 'usuarios' table,
    fetches the results, and prints each user's data.

    """
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()

    c.execute('''SELECT * FROM usuarios''')
    usuarios = c.fetchall()

    for usuario in usuarios:
        print(usuario)

    conn.close()

if __name__ == "__main__":
    show_database()