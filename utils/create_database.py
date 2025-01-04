import os
from dotenv import load_dotenv

from main import app, db
from utils import logger


load_dotenv()
db_path = os.getenv("DB_PATH")


if not os.path.exists(db_path):
    with app.app_context():
        db.create_all()
        logger.info("database created successfully")
else:
    logger.info("database already exists")
