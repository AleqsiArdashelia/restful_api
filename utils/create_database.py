# Importing necessary modules
import os  # For interacting with the operating system
from dotenv import load_dotenv  # For loading environment variables from a .env file

# Importing the Flask app and SQLAlchemy database instance from the main module
from main import app, db

# Importing the logger utility for logging information
from utils import logger

# Load environment variables from the .env file
load_dotenv()

# Retrieve the database path from the environment variables
db_path = os.getenv("DB_PATH")

# Check if the database file exists
if not os.path.exists(db_path):
    # If the database does not exist, create it within the app context
    with app.app_context():
        db.create_all()  # Create all tables defined in the SQLAlchemy models
        logger.info("database created successfully")  # Log success message
else:
    # If the database already exists, log a message
    logger.info("database already exists")