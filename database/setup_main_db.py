# database/setup_main_db.py

from database.db_connection import get_db_connection
from config.db_config import DB_CONFIG

import os
import psycopg
from psycopg import sql
from dotenv import load_dotenv
import logging
import re
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database_if_not_exists(connection, dbname):
    """Create the target database if it doesn't exist."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
            if not cursor.fetchone():
                logger.info(f"Database '{dbname}' does not exist. Creating it now.")
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
                logger.info(f"Database '{dbname}' created successfully.")
            else:
                logger.info(f"Database '{dbname}' already exists.")
    except Exception as e:
        logger.error(f"Error while creating database: {e}")
        raise

def create_schema_if_not_exists(connection, schema_name):
    """Create the schema if it doesn't exist."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", (schema_name,))
            if not cursor.fetchone():
                logger.info(f"Schema '{schema_name}' does not exist. Creating it now.")
                cursor.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema_name)))
                logger.info(f"Schema '{schema_name}' created successfully.")
            else:
                logger.info(f"Schema '{schema_name}' already exists.")
    except Exception as e:
        logger.error(f"Error while creating schema: {e}")
        raise

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

def setup_database():
    """Set up the database, schema, and tables."""
    # Connect to the default 'postgres' database to create the target database
    connection = get_db_connection(dbname="postgres")
    if connection is None:
        return

    # Create the target database if it doesn't exist
    create_database_if_not_exists(connection, DB_CONFIG["dbname"])
    connection.close()

    # Connect to the target database
    connection = get_db_connection()
    if connection is None:
        return

    # Create schema and tables
    create_schema_if_not_exists(connection, "api_data")
    create_news_articles_table(connection)
    alter_news_articles_table(connection)
    connection.close()

if __name__ == "__main__":
    setup_database()
    logger.info("Database and schema setup completed successfully.")