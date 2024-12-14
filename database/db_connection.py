# database/db_connection.py

import psycopg
import logging
import os
from time import sleep
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Context manager for database connections."""
    def __init__(self):
        self.connection = None

    def __enter__(self):
        """Get database connection."""
        connection_params = {
            'dbname': os.getenv('POSTGRES_DB'),
            'user': os.getenv('POSTGRES_USER'),
            'password': os.getenv('POSTGRES_PASSWORD'),
            'host': 'localhost' if os.getenv('TEST_ENV') else os.getenv('POSTGRES_HOST', 'db'),
            'port': int(os.getenv('POSTGRES_PORT', 5432))
        }

        try:
            logger.info(f"Connecting to database at {connection_params['host']}:{connection_params['port']}")
            self.connection = psycopg.connect(**connection_params)
            return self.connection
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection."""
        if self.connection:
            try:
                if exc_type is None:
                    self.connection.commit()
                self.connection.close()
                self.connection = None
            except Exception as e:
                logger.error(f"Error closing connection: {str(e)}")

def get_db_connection(dbname=None):
    try:
        conn = psycopg.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            dbname=dbname or os.getenv("POSTGRES_DB")
        )
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise

# database/setup_main_db.py

from database.db_connection import get_db_connection

def setup_database():
    connection = get_db_connection(dbname=ADMIN_DB_CONFIG["dbname"])
    cursor = connection.cursor()
    # Your database setup code here
    connection.commit()
    connection.close()

if __name__ == "__main__":
    setup_database()
