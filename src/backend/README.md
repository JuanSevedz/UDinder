# FastAPI Backend

This project is a backend API built with FastAPI. It provides endpoints for user management, profile management, matching users, messaging, and administrative actions. Below is a summary of the available endpoints and their functionalities.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
  - [Users](#users)
  - [Profiles](#profiles)
  - [Matches](#matches)
  - [Messages](#messages)
  - [Administration](#administration)
- [Running the Application](#running-the-application)

## Installation

To install and run this project, you'll need Python 3.11 and pip (Python package installer). Follow the steps below:

1. Clone the repository:
    ```sh
    git clone https://github.com/JuanSevedz/UDinder.git
    cd yourproject
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

The backend provides a set of RESTful API endpoints to manage users, profiles, matches, messages, and administrative tasks.

## Endpoints

### Users

- `POST /register`: Register a new user
- `POST /login`: User login
- `POST /logout`: User logout
- `GET /users/{user_id}`: Get user by ID
- `PUT /users/{user_id}`: Update user by ID
- `DELETE /users/{user_id}`: Delete user by ID

### Profiles

- `GET /profiles/{user_id}`: Get profile by user ID
- `PUT /profiles/{user_id}`: Update profile by user ID

### Matches

- `GET /matches/{user_id}`: Get matches for user by ID
- `POST /matches`: Create a new match
- `DELETE /matches/{match_id}`: Delete match by ID

### Messages

- `POST /messages`: Send a new message
- `GET /messages/{conversation_id}`: Get messages by conversation ID
- `DELETE /messages/{message_id}`: Delete message by ID

### Administration

- `GET /admin/reports`: Get user reports
- `POST /admin/block_user/{user_id}`: Block user by ID
- `POST /admin/unblock_user/{user_id}`: Unblock user by ID

## Running the Application

To start the FastAPI server, run the following command:

```sh
python main.py
