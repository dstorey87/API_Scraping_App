# database/setup_main_db.py

from database.db_connection import get_db_connection
from config.db_config import DB_CONFIG, ADMIN_DB_CONFIG
import os
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

def check_test_data_exists(cursor):
    cursor.execute("SELECT COUNT(*) FROM articles WHERE source = 'Test Source'")
    return cursor.fetchone()[0] > 0

def setup_database():
    # First connect to admin database to create new DB if needed
    admin_conn = get_db_connection(dbname=os.getenv("POSTGRES_ADMIN_DB"))
    admin_conn.autocommit = True
    cursor = admin_conn.cursor()

    try:
        # Create main database if it doesn't exist
        main_db = os.getenv("POSTGRES_DB")
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{main_db}'")
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {main_db}")
            logger.info(f"Created database {main_db}")
    finally:
        cursor.close()
        admin_conn.close()

    # Now connect to main database to create tables
    main_conn = get_db_connection()
    cursor = main_conn.cursor()

    try:
        # Create your tables here
        create_tables_sql = """
        CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT,
            source VARCHAR(50),
            published_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS guardian_articles (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            publication_date TIMESTAMP NOT NULL
        );
        """
        cursor.execute(create_tables_sql)
        main_conn.commit()
        logger.info("Database tables created successfully")

        # Insert test data if it doesn't exist
        if not check_test_data_exists(cursor):
            cursor.execute("""
                INSERT INTO articles (title, content, source)
                VALUES ('Test Title', 'Test Content', 'Test Source');
            """)

            cursor.execute("""
                INSERT INTO guardian_articles (title, url, publication_date)
                VALUES (
                    'Guardian Test',
                    'https://www.theguardian.com/test-article',
                    CURRENT_TIMESTAMP
                );
            """)
            main_conn.commit()
            logger.info("Test data inserted successfully")

    finally:
        cursor.close()
        main_conn.close()
        logger.info("Database and schema setup completed successfully.")

if __name__ == "__main__":
    setup_database()
    logger.info("Database and schema setup completed successfully.")