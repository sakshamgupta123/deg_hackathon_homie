import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs('app/logs', exist_ok=True)

# Create a formatter that includes timestamp, logger name, and level
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Define the log file path
log_filename = 'app/logs/progress.log'

# Remove the old log file if it exists
if os.path.exists(log_filename):
    try:
        os.remove(log_filename)
    except Exception:
        pass  # If we can't remove it, we'll just create a new file

# Create and configure the file handler
file_handler = logging.FileHandler(log_filename, mode='w')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Configure the root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Remove any existing handlers to avoid duplicate logs
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Add our configured handler
root_logger.addHandler(file_handler)


def get_logger(name):
    """Get a logger with the specified name."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger