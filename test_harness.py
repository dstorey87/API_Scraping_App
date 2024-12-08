# test_harness.py

import unittest
import logging
import os
import psycopg
from datetime import datetime
from dotenv import load_dotenv
from api.fetch_news_api import fetch_news
from api.fetch_guardian_api import fetch_guardian_data
from api.fetch_pytrends import fetch_trending_topics
from api.fetch_reddit_data import fetch_reddit_data
from database.db_connection import get_db_connection, DatabaseConnection
from database.insert_data import insert_news_articles
from psycopg.errors import UniqueViolation

# Load environment variables
load_dotenv()

# Set test environment
os.environ['TEST_ENV'] = 'true'

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
                else:
                    self.connection.rollback()
                self.connection.close()
            except Exception as e:
                logger.error(f"Error closing connection: {str(e)}")

def get_db_connection():
    """Get database connection using context manager."""
    return DatabaseConnection().__enter__()

def close_db_connection(connection):
    """Close database connection safely."""
    if connection:
        try:
            connection.close()
        except Exception as e:
            logger.error(f"Error closing connection: {str(e)}")

class BaseTestCase(unittest.TestCase):
    """Base test case with database connection handling."""
    
    def setUp(self):
        """Setup before each test."""
        self.db = DatabaseConnection()
        self.connection = self.db.__enter__()
        if not self.connection and 'db_' in self._testMethodName:
            self.skipTest("Database connection not available")
            
    def tearDown(self):
        """Cleanup after each test."""
        if hasattr(self, 'db'):
            self.db.__exit__(None, None, None)

class TestAPIModules(BaseTestCase):
    """Test case for API modules."""
    
    def setUp(self):
        """Setup before each test."""
        super().setUp()
        self.connection = get_db_connection()
        if not self.connection and 'db_' in self._testMethodName:
            self.skipTest("Database connection not available")

    def test_fetch_news(self):
        keywords = ['technology', 'science']
        news = fetch_news(keywords)
        self.assertIsInstance(news, list)
        self.assertGreater(len(news), 0)
        logger.info("fetch_news test passed.")
    
    def test_fetch_guardian_data(self):
        guardian_data = fetch_guardian_data()
        self.assertIsInstance(guardian_data, list)
        self.assertGreater(len(guardian_data), 0)
        logger.info("fetch_guardian_data test passed.")
    
    def test_fetch_trending_topics(self):
        trending = fetch_trending_topics()
        self.assertIsInstance(trending, list)
        self.assertGreater(len(trending), 0)
        logger.info("fetch_trending_topics test passed.")
    
    def test_fetch_reddit_data(self):
        reddit_data = fetch_reddit_data()
        self.assertIsInstance(reddit_data, list)
        self.assertGreater(len(reddit_data), 0)
        logger.info("fetch_reddit_data test passed.")

    def test_rate_limiting(self):
        """Test API rate limit handling."""
        # Test multiple rapid requests
        for _ in range(5):
            news = fetch_news(['technology'])
            self.assertIsInstance(news, list)
            # Verify we're getting results despite rapid requests
            self.assertGreater(len(news), 0)
        logger.info("Rate limiting test passed.")

class TestDatabaseModules(BaseTestCase):
    """Test case for database modules."""
    
    def test_db_connection(self):
        connection = get_db_connection()
        self.assertIsNotNone(connection)
        connection.close()
        logger.info("get_db_connection test passed.")
    
    def test_insert_news_articles(self):
        connection = get_db_connection()
        self.assertIsNotNone(connection)
        try:
            with connection:
                with connection.cursor() as cursor:
                    sample_article = {
                        "source": "Guardian",
                        "author": "John Doe",
                        "title": "Sample News",
                        "description": "This is a sample news article.",
                        "url": "https://example.com/sample-news",
                        "published_at": "2024-12-07 12:00:00"
                    }
                    insert_news_articles(connection, [sample_article])
                    cursor.execute("SELECT * FROM api_data.news_articles WHERE url = %s", ("https://example.com/sample-news",))
                    result = cursor.fetchone()
                    self.assertIsNotNone(result)
            logger.info("insert_news_articles test passed.")
        except Exception as e:
            self.fail(f"Exception occurred: {e}")
        finally:
            connection.close()

    def test_error_handling(self):
        """Test database error handling."""
        connection = get_db_connection()
        try:
            # Test duplicate entry handling
            sample_article = {
                "source": "Test",
                "author": "Test Author",
                "title": "Test Title",
                "description": "Test Description",
                "url": "https://test.com/article",
                "published_at": "2024-01-01 00:00:00"
            }
            
            # Insert same article twice to test UniqueViolation handling
            insert_news_articles(connection, [sample_article])
            insert_news_articles(connection, [sample_article])
            
            # Test connection retry logic
            connection.close()
            new_connection = get_db_connection()
            self.assertIsNotNone(new_connection)
            logger.info("Database error handling test passed.")
        
        except UniqueViolation:
            logger.info("Successfully caught duplicate entry")
        finally:
            connection.close()
        
    def test_data_cleaning(self):
        """Test data validation and cleaning."""
        connection = get_db_connection()
        try:
            # Test with complete valid article
            valid_article = {
                "source": "Test",
                "author": "Test Author",
                "title": "Test Title",
                "description": "Test Description",
                "url": "https://test.com/article1",
                "published_at": "2024-01-01 00:00:00"
            }
            
            # Test with missing optional fields
            incomplete_article = {
                "source": "Test",
                "title": "Test Title",
                "url": "https://test.com/article2"  # Only required fields
            }
            
            # Insert both articles
            insert_news_articles(connection, [valid_article, incomplete_article])
            
            # Verify data cleaning
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM api_data.news_articles 
                    WHERE source = 'Test' 
                    AND url IN (%s, %s)
                """, ("https://test.com/article1", "https://test.com/article2"))
                results = cursor.fetchall()
                self.assertEqual(len(results), 2)  # Both articles should be inserted
                
            logger.info("Data cleaning test passed.")
        
        finally:
            if connection:
                connection.close()

    def test_trending_topics_db(self):
        """Test trending topics insertion and retrieval."""
        connection = get_db_connection()
        topics = ['tech', 'science']
        
        try:
            with connection.cursor() as cursor:
                # Clean up any existing test data first
                cursor.execute("""
                    DELETE FROM api_data.trending_topics 
                    WHERE topic = ANY(%s)
                """, (topics,))  # Pass list directly
                connection.commit()

                # Insert test topics
                for topic in topics:
                    cursor.execute("""
                        INSERT INTO api_data.trending_topics (topic, score)
                        VALUES (%s, %s)
                    """, (topic, 100))
                connection.commit()
                
                # Verify insertion
                cursor.execute("""
                    SELECT * FROM api_data.trending_topics 
                    WHERE topic = ANY(%s)
                """, (topics,))  # Pass list directly
                results = cursor.fetchall()
                self.assertEqual(len(results), len(topics), 
                               f"Expected {len(topics)} test topics, got {len(results)}")

                # Clean up test data
                cursor.execute("""
                    DELETE FROM api_data.trending_topics 
                    WHERE topic = ANY(%s)
                """, (topics,))
                connection.commit()
                
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()

class TestEndToEnd(BaseTestCase):
    """End-to-End test case for the entire data flow."""
    
    def test_full_pipeline(self):
        """Test the complete data pipeline."""
        try:
            # Get trending topics
            trending_topics = fetch_trending_topics()
            self.assertIsInstance(trending_topics, list)
            self.assertGreater(len(trending_topics), 0)
            
            # Get articles from all sources
            keywords = trending_topics[:5]
            news_articles = fetch_news(keywords)
            guardian_articles = fetch_guardian_data()
            reddit_articles = fetch_reddit_data()
            
            # Verify article lists
            self.assertIsInstance(news_articles, list)
            self.assertIsInstance(guardian_articles, list)
            self.assertIsInstance(reddit_articles, list)
            
            # Insert articles using DatabaseConnection context manager
            with DatabaseConnection() as connection:
                if not connection:
                    self.fail("Could not establish database connection")
                    
                # Process and insert articles
                valid_articles = [
                    (
                        str(article.get('source', '')),
                        str(article.get('author', '')),
                        str(article.get('title', '')),
                        str(article.get('description', '')),
                        str(article.get('url', '')),
                        article.get('published_at')
                    )
                    for article in news_articles 
                    if article.get('title') and article.get('url')
                ]
                
                if valid_articles:
                    with connection.cursor() as cursor:
                        cursor.executemany("""
                            INSERT INTO api_data.news_articles 
                            (source, author, title, description, url, published_at)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON CONFLICT (url) DO NOTHING
                        """, valid_articles)
                    connection.commit()
                
                logger.info("Full pipeline test passed.")
                
        except Exception as e:
            self.fail(f"Exception during pipeline test: {e}")

if __name__ == "__main__":
    unittest.main()
