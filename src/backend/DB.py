"""Generate and save fake user data to an SQLite database.

This script generates fake user data using the Faker library and saves it to an SQLite 
database.
It creates a table named 'usuarios' with columns for id, username, email, and password.
Then it generates 10 fake user records, each with a randomly generated username, email, 
and password.
The passwords are stored as plaintext, without hashing.

"""
import sqlite3
import os  # Import the os module
from faker import Faker

# Create an instance of Faker
fake = Faker()

# Get the absolute path of the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Combine the current directory path with the database file name
db_path = os.path.join(current_directory, "usuarios.db")

# Create a connection to the SQLite database
conn = sqlite3.connect(db_path)
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
for _ in range(10):
    username = fake.user_name()
    email = fake.email()
    password = fake.password()
    c.execute(
        """INSERT INTO usuarios (username, email, password)
                 VALUES (?, ?, ?)""",
        (username, email, password),
    )

# Save changes and close the connection
conn.commit()
conn.close()
