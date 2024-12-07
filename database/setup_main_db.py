# database/setup_main_db.py

from database.db_connection import get_db_connection
from config.db_config import DB_CONFIG, ADMIN_DB_CONFIG

import psycopg
from psycopg import sql
import logging

# Configure logging with detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_database_if_not_exists(connection, dbname):
    """Create the target database if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
            connection.commit()
            logger.info(f"Database '{dbname}' created successfully.")
        else:
            logger.info(f"Database '{dbname}' already exists.")
    except Exception as e:
        logger.error(f"Error creating database '{dbname}': {e}")
        connection.rollback()

def create_schema_if_not_exists(connection, schema_name):
    """Create the schema if it doesn't exist."""
    create_schema_query = sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(schema_name))
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_schema_query)
            connection.commit()
            logger.info(f"Schema '{schema_name}' created successfully.")
    except Exception as e:
        logger.error(f"Error creating schema '{schema_name}': {e}")
        connection.rollback()

def create_news_articles_table(connection):
    """Create the news_articles table in the api_data schema."""
    create_table_query = """
        CREATE TABLE IF NOT EXISTS api_data.news_articles (
            id SERIAL PRIMARY KEY,
            source TEXT,
            author TEXT,
            title TEXT,
            description TEXT,
            url TEXT UNIQUE,
            published_at TIMESTAMP
        );
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
            connection.commit()
            logger.info("Table 'api_data.news_articles' is set up successfully.")
    except Exception as e:
        logger.error(f"Error setting up the table: {e}")
        connection.rollback()

def alter_news_articles_table(connection):
    """Alter the news_articles table to adjust column data types."""
    alter_table_query = """
        ALTER TABLE api_data.news_articles
        ALTER COLUMN source TYPE TEXT,
        ALTER COLUMN author TYPE TEXT,
        ALTER COLUMN title TYPE TEXT,
        ALTER COLUMN description TYPE TEXT,
        ALTER COLUMN url TYPE TEXT;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(alter_table_query)
            connection.commit()
            logger.info("Table 'api_data.news_articles' altered successfully.")
    except Exception as e:
        logger.error(f"Error altering table: {e}")
        connection.rollback()

def setup_schema(connection):
    """Create the necessary database schema."""
    try:
        cursor = connection.cursor()
        
        # Example schema creation
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS guardian_articles (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            publication_date TIMESTAMP NOT NULL
        );
        """)
        
        connection.commit()
        cursor.close()
        print("Schema setup completed successfully.")
    except Exception as error:
        print(f"Error setting up schema: {error}")
        connection.rollback()

def setup_database():
    """Set up the database, schema, and tables."""
    # Connect to the admin database using ADMIN_DB_CONFIG
    connection = get_db_connection(dbname=ADMIN_DB_CONFIG["dbname"])
    if connection is None:
        logger.error("Failed to connect to the admin database.")
        return

    # Create the target database if it doesn't exist
    create_database_if_not_exists(connection, DB_CONFIG["dbname"])
    connection.close()

    # Connect to the target database
    connection = get_db_connection()
    if connection is None:
        logger.error("Failed to connect to the target database.")
        return

    # Create schema and tables
    create_schema_if_not_exists(connection, "api_data")
    create_news_articles_table(connection)
    alter_news_articles_table(connection)
    setup_schema(connection)
    connection.close()

if __name__ == "__main__":
    setup_database()
    logger.info("Database and schema setup completed successfully.")