# Import the logging module to enable logging functionality
import logging

# Configure the basic settings for the logging system
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO (logs INFO, WARNING, ERROR, and CRITICAL messages)
    format='%(asctime)s  [%(levelname)s]: %(message)s',  # Define the format of the log messages
    # '%(asctime)s' logs the timestamp of the message
    # '%(levelname)s' logs the severity level (e.g., INFO, ERROR)
    # '%(message)s' logs the actual message
    datefmt='%Y-%m-%d %H:%M:%S'  # Specify the format for timestamps (e.g., 2025-01-04 12:34:56)
)

# Create a logger object for the current module
# The logger is identified by the module's name (retrieved using __name__)
logger = logging.getLogger(__name__)
