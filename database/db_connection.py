# database/db_connection.py

import psycopg
from psycopg import sql
from config import db_config
import logging
import time
from config.db_config import DB_CONFIG
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_to_db():
    try:
        connection = psycopg.connect(
            user=db_config.POSTGRES_USER,
            password=db_config.POSTGRES_PASSWORD,
            host=db_config.POSTGRES_HOST,
            port=db_config.POSTGRES_PORT,
            database=db_config.POSTGRES_DB
        )
        return connection
    except Exception as error:
        print(f"Error connecting to database: {error}")
        return None

def close_db_connection(connection):
    if connection:
        connection.close()

def get_db_connection(dbname=None, retries=3, delay=5):
    """Establish a connection to the PostgreSQL database."""
    db_config = DB_CONFIG.copy()
    if dbname:
        db_config["dbname"] = dbname

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
