"""Generate and save fake user data to an SQLite database.

This script generates fake user data using the Faker library and saves it to an SQLite 
database.
It creates a table named 'usuarios' with columns for id, username, email, and password.
Then it generates 10 fake user records, each with a randomly generated username, email, 
and password.
The passwords are stored as plaintext, without hashing.

"""

import sqlite3
from faker import Faker  # Importar la clase Faker

# Create an instance of Faker
fake = Faker()

# Create a connection to the SQLite database
conn = sqlite3.connect("usuarios.db")
c = conn.cursor()

# Create the 'usuarios' table if it doesn't exist
c.execute(
    """CREATE TABLE IF NOT EXISTS usuarios
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT,
              email TEXT,
              password TEXT)"""
)

# Generate and save fake user data
for _ in range(10): #(#)number of users wished
    username = fake.user_name()
    email = fake.email()
    password = fake.password()  # Save the password whithout hash

     # Insert the data into the 'usuarios' table
    c.execute(
        """INSERT INTO usuarios (username, email, password)
                 VALUES (?, ?, ?)""",
        (username, email, password),
    )

# Save and pull changes
conn.commit()
conn.close()