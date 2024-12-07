# config/error_logging.py

import logging
from logging.handlers import RotatingFileHandler
from database.db_connection import get_db_connection
import time

def get_db_connection_with_retry(dbname=None, retries=3, delay=5):
    """Enhanced database connection with retry logic."""
    connection = None
    for attempt in range(retries):
        try:
            connection = get_db_connection(dbname)
            break
        except Exception as e:
            logging.warning(f"Connection attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    if connection is None:
        logging.error("Failed to connect to the database after multiple attempts.")
    return connection

def setup_logging():
    """Setup centralized logging."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    handler = RotatingFileHandler('logs/app.log', maxBytes=1000000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logger.addHandler(console)

setup_logging()