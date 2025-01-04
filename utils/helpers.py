# Importing necessary modules from Flask-RESTful
from flask_restful import fields, reqparse

# Define a dictionary that maps the fields of the `DatabaseModel` to their types
# This will be used for serializing the database objects into a JSON format
user_table_dict = {
    'id': fields.Integer,       # ID of the user, an integer field
    'username': fields.String,  # Username of the user, a string field
    'email': fields.String,     # Email of the user, a string field
    'password': fields.String,  # Password of the user, a string field
    'created_at': fields.DateTime  # Timestamp when the user was created
}

# Define a function to parse incoming request arguments for user-related operations
def get_user_args():
    # Initialize a RequestParser to handle request arguments
    user_args = reqparse.RequestParser()

    # Define a list of required fields for user input
    necessary_cols = ['username', 'email', 'password']

    # Iterate over the required fields and add them to the RequestParser
    for col_name in necessary_cols:
        user_args.add_argument(
            col_name,              # Name of the argument (e.g., "username", "email", etc.)
            type=str,              # Specify that the argument must be of type string
            required=True,         # Mark the argument as required (must be present in the request)
            help=f"{col_name} column can not be empty"  # Custom error message if the argument is missing
        )

    # Return the configured RequestParser object
    return user_args
