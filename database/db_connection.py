# database/db_connection.py

import os
import psycopg
import logging
import time
from config.db_config import DB_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection(dbname=None, retries=3, delay=5):
    """Establish a connection to the PostgreSQL database."""
    # Create a copy of the DB_CONFIG to avoid modifying the original
    db_config = DB_CONFIG.copy()
    
    # Override the database name if dbname is provided
    if dbname:
        db_config["dbname"] = dbname

    # Override the host if provided as an environment variable
    db_config["host"] = os.getenv("POSTGRES_HOST", db_config["host"])

    for attempt in range(1, retries + 1):
        try:
            logger.info(f"Attempt {attempt}: Connecting to the database at {db_config['host']}:{db_config['port']}")
            connection = psycopg.connect(**db_config)
            logger.info("Database connection established successfully.")
            return connection
        except psycopg.OperationalError as e:
            logger.error(f"Database connection error: {e}")
            if attempt < retries:
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.error("Max retries reached. Could not connect to the database.")
                return None
