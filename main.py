# Importing necessary modules
from flask import Flask  # Core Flask framework
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy for database integration
from flask_restful import Resource, Api, marshal_with, abort  # Flask-RESTful for building REST APIs

import os  # To interact with the operating system (e.g., read environment variables)
from dotenv import load_dotenv  # For loading environment variables from a .env file
from datetime import datetime  # For handling timestamps
from werkzeug.security import generate_password_hash  # To securely hash passwords

# Import utility functions from utils module
from utils import user_table_dict, get_user_args

# Load environment variables from .env file
load_dotenv()

# Retrieve the database URI from the environment variables
db_uri = os.getenv("SQLALCHEMY_DATABASE_URI")

# Parse user input arguments (e.g., username, email, password)
user_args = get_user_args()

# Initialize the Flask app
app = Flask(__name__)

# Configure the database URI for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

# Initialize the SQLAlchemy database object
db = SQLAlchemy(app)

# Initialize the Flask-RESTful API
api = Api(app)

# Define the database model for a user
class DatabaseModel(db.Model):
    # Define table columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(25), unique=True, nullable=False)  # Unique username
    email = db.Column(db.String(25), unique=True, nullable=False)  # Unique email address
    password = db.Column(db.String(25), nullable=False)  # User password (hashed)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for record creation

# Helper function to validate user data
def validate_user_data(username, email, password):
    # Check if the username already exists
    if DatabaseModel.query.filter_by(username=username).first():
        abort(400, message="username already exists")  # Abort with HTTP 400 and error message

    # Check if the email already exists or is invalid
    if DatabaseModel.query.filter_by(email=email).first():
        abort(400, message="this email already exists")
    elif "@" not in email:
        abort(400, message="email format is not valid")

    # Check if the password is at least 8 characters long
    if len(password) < 8:
        abort(400, message="password must contain at least 8 characters")

# Define a resource for managing all users
class AllUsers(Resource):
    # GET method to retrieve all users
    @marshal_with(user_table_dict)  # Automatically formats the response
    def get(self):
        users = DatabaseModel.query.all()  # Fetch all users from the database
        return users

    # POST method to create a new user
    @marshal_with(user_table_dict)
    def post(self):
        args = user_args.parse_args()  # Parse incoming arguments

        # Extract user details from the parsed arguments
        username = args["username"].lower()
        email = args["email"].lower()
        password = args["password"]

        # Validate the provided user data
        validate_user_data(username, email, password)

        # Create a new user record
        user = DatabaseModel(
            username=username,
            email=email,
            password=generate_password_hash(password)  # Hash the password before storing
        )
        db.session.add(user)  # Add the user to the database session
        db.session.commit()  # Commit the session to save changes

        # Return all users, including the newly created one
        users = DatabaseModel.query.all()
        return users, 201  # HTTP 201 Created

# Add the AllUsers resource to the API at the root endpoint
api.add_resource(AllUsers, '/')

# Define a resource for managing individual users
class IndividualUser(Resource):
    # GET method to retrieve a user by ID
    @marshal_with(user_table_dict)
    def get(self, id):
        user = DatabaseModel.query.filter_by(id=id).first()  # Fetch user by ID

        if not user:  # If user does not exist, abort with HTTP 404
            abort(404, message="user does not exist")
        return user

    # PATCH method to update a user by ID
    @marshal_with(user_table_dict)
    def patch(self, id):
        args = user_args.parse_args()  # Parse incoming arguments
        user = DatabaseModel.query.filter_by(id=id).first()  # Fetch user by ID

        if not user:  # If user does not exist, abort with HTTP 404
            abort(404, message="user does not exist")

        # Update user details with the new data
        username = args["username"].lower()
        email = args["email"].lower()
        password = args["password"]

        # Validate the new user data
        validate_user_data(username, email, password)

        # Update the user record
        user.username = username
        user.email = email
        user.password = generate_password_hash(password)

        db.session.commit()  # Commit the session to save changes
        return user

    # DELETE method to remove a user by ID
    @marshal_with(user_table_dict)
    def delete(self, id):
        user = DatabaseModel.query.filter_by(id=id).first()  # Fetch user by ID

        if not user:  # If user does not exist, abort with HTTP 404
            abort(404, message="user does not exist")

        db.session.delete(user)  # Delete the user record
        db.session.commit()  # Commit the session to save changes

        # Return all remaining users
        users = DatabaseModel.query.all()
        return users

# Add the IndividualUser resource to the API with a dynamic <id> parameter
api.add_resource(IndividualUser, '/user_info/<int:id>')

# Entry point for running the application
if __name__ == '__main__':
    app.run(debug=False)  # Start the Flask development server
