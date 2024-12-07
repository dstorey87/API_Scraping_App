# test_harness.py

import unittest
import logging
from api.fetch_news_api import fetch_news
from api.fetch_guardian_api import fetch_guardian_data
from api.fetch_pytrends import fetch_trending_topics
from api.fetch_reddit_data import fetch_reddit_data
from database.db_connection import get_db_connection
from database.insert_data import insert_news_articles
from psycopg.errors import UniqueViolation  # type: ignore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestAPIModules(unittest.TestCase):
    """Test case for API modules."""
    
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

class TestDatabaseModules(unittest.TestCase):
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

class TestEndToEnd(unittest.TestCase):
    """End-to-End test case for the entire data flow."""
    
    def test_full_pipeline(self):
        trending_topics = fetch_trending_topics()
        self.assertIsInstance(trending_topics, list)
        self.assertGreater(len(trending_topics), 0)
        
        keywords = trending_topics[:5]
        news_articles = fetch_news(keywords)
        self.assertIsInstance(news_articles, list)
        self.assertGreater(len(news_articles), 0)
        
        guardian_articles = fetch_guardian_data()
        self.assertIsInstance(guardian_articles, list)
        self.assertGreater(len(guardian_articles), 0)
        
        reddit_articles = fetch_reddit_data()
        self.assertIsInstance(reddit_articles, list)
        self.assertGreater(len(reddit_articles), 0)
        
        all_articles = news_articles + guardian_articles + reddit_articles
        connection = get_db_connection()
        self.assertIsNotNone(connection, "Failed to establish database connection.")
        
        try:
            with connection:
                insert_news_articles(connection, all_articles)
                with connection.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM api_data.news_articles")
                    count = cursor.fetchone()[0]
                    self.assertGreater(count, 0)
            logger.info("Full pipeline test passed.")
        except Exception as e:
            self.fail(f"Exception occurred during full pipeline test: {e}")
        finally:
            connection.close()

if __name__ == "__main__":
    unittest.main()