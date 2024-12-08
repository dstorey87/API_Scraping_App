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
            self.connection.close()
            
def get_db_connection():
    """Get database connection using context manager."""
    return DatabaseConnection().__enter__()

def close_db_connection(connection):
    if connection:
        connection.close()
