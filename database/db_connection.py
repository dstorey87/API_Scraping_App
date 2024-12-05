import psycopg
from config.db_config import DB_CONFIG

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    return psycopg.connect(**DB_CONFIG)
