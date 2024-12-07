import psycopg
from psycopg import sql
from psycopg.errors import UniqueViolation
import logging
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def insert_news_articles(connection, articles):
    """Insert news articles into the database."""
    try:
        with connection.cursor() as cursor:
            for article in articles:
                required_fields = ["source", "author", "title", "description", "url", "published_at"]
                if all(field in article for field in required_fields):
                    # Ensure 'published_at' is a datetime object
                    if isinstance(article["published_at"], str):
                        article["published_at"] = datetime.fromisoformat(article["published_at"])
                    
                    cursor.execute(
                        """
                        INSERT INTO api_data.news_articles (source, author, title, description, url, published_at)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (url) DO NOTHING
                        """,
                        (
                            article["source"],
                            article["author"],
                            article["title"],
                            article["description"],
                            article["url"],
                            article["published_at"]
                        )
                    )
                else:
                    logger.warning("News article missing required fields. Skipping.")
        connection.commit()
        logger.info("All news articles inserted successfully.")
    except Exception as e:
        connection.rollback()
        logger.error(f"Error inserting news articles: {e}")

def insert_guardian_articles(connection, articles):
    """Insert Guardian articles into the database."""
    if connection is None:
        logger.error("No database connection available.")
        return

    try:
        with connection.cursor() as cursor:
            for article in articles:
                # Data validation: Ensure required fields are present
                headline = article.get("headline")
                url = article.get("url")
                publication_date = article.get("publication_date")
                if not headline or not url or not publication_date:
                    logger.warning("Guardian article missing required fields. Skipping.")
                    continue

                # Prepare SQL query using psycopg's sql module for safety
                insert_query = sql.SQL("""
                    INSERT INTO api_data.guardian_articles (headline, url, publication_date)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (url) DO NOTHING;
                """)

                try:
                    # Execute query with provided parameters
                    cursor.execute(
                        insert_query, (
                            headline,
                            url,
                            publication_date
                        )
                    )
                except UniqueViolation:
                    logger.warning(f"Duplicate entry detected for URL: {url}. Skipping insertion.")
                except Exception as e:
                    logger.error(f"Error inserting Guardian article '{headline}': {e}")
            # Commit the transaction after all insertions
            connection.commit()
            logger.info("All Guardian articles inserted successfully.")
    except Exception as e:
        logger.error(f"Error inserting Guardian articles: {e}")
        connection.rollback()

def insert_reddit_articles(connection, articles):
    """Insert Reddit articles into the database."""
    try:
        with connection.cursor() as cursor:
            for article in articles:
                if all(key in article for key in ["title", "score", "url", "created_at"]):
                    if not isinstance(article["created_at"], datetime):
                        article["created_at"] = datetime.fromtimestamp(article["created_at"])
                    
                    cursor.execute(
                        """
                        INSERT INTO api_data.reddit_articles (title, score, url, created_at)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (url) DO NOTHING
                        """,
                        (
                            article["title"],
                            article["score"],
                            article["url"],
                            article["created_at"]
                        )
                    )
                else:
                    logger.warning("Reddit article missing required fields. Skipping.")
        connection.commit()
        logger.info("All Reddit articles inserted successfully.")
    except Exception as e:
        connection.rollback()
        logger.error(f"Error inserting Reddit articles: {e}")
