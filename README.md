# RESTful API for User Management

## Overview
This project is a RESTful API designed to manage user data. It allows creating, retrieving, updating, and deleting user records in a database. The application is built using Flask, Flask-RESTful, and SQLAlchemy, following modular design principles for better maintainability and scalability.

---

## Features

- **User Management**:
  - **Retrieve All Users**: Get a list of all users.
  - **Retrieve Individual User**: Get detailed information about a specific user by ID.
  - **Create User**: Add a new user to the database.
  - **Update User**: Modify existing user details.
  - **Delete User**: Remove a user from the database.

- **Input Validation**:
  - Ensures username, email, and password follow specific constraints.
  - Validates email format and checks for duplicates in the database.
  - Enforces a minimum password length of 8 characters.

- **Database Integration**: Uses SQLAlchemy for ORM and database management.

- **Logging**: Centralized logging for tracking database creation and API actions.

---


## Setup Instructions

### Prerequisites
1. Python 3.7+
2. Flask
3. Flask-RESTful
4. Flask-SQLAlchemy
5. Python-dotenv

### Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd project
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables:
    - Create a `.env` file in the root directory.
    - Add the following variables:
      ```env
      SQLALCHEMY_DATABASE_URI="sqlite:///database.db"
      DB_PATH="\path\to\database" # direct to project root directory
      ```

5. Initialize the database:
    ```bash
    python utils/create_database.py
    ```

6. Run the application:
    ```bash
    python main.py
    ```

---

## API Endpoints

### Base URL: `/`

### Resources

#### **`GET /`**
- Retrieves a list of all users.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "password": "hashed_password",
      "created_at": "2025-01-01T12:00:00"
    }
  ]
  ```

#### **`POST /`**
- Creates a new user.
- **Request Body**:
  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword"
  }
  ```
- **Response**: Returns a list of all users including the newly created user.

#### **`GET /user_info/<int:id>`**
- Retrieves details of a specific user by ID.
- **Response**:
  ```json
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "password": "hashed_password",
    "created_at": "2025-01-01T12:00:00"
  }
  ```

#### **`PATCH /user_info/<int:id>`**
- Updates details of a specific user.
- **Request Body**:
  ```json
  {
    "username": "new_username",
    "email": "new_email@example.com",
    "password": "newpassword"
  }
  ```

#### **`DELETE /user_info/<int:id>`**
- Deletes a specific user by ID.
- **Response**: Returns the updated list of users.

---

## Testing

You can test the API endpoints using tools like:
- [Postman](https://www.postman.com/)
- [cURL](https://curl.se/)