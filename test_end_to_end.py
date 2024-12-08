# test_end_to_end.py

import unittest
import logging
import os
from dotenv import load_dotenv
from api.fetch_news_api import fetch_news
from api.fetch_guardian_api import fetch_guardian_data
from api.fetch_pytrends import fetch_trending_topics
from api.fetch_reddit_data import fetch_reddit_data
from database.db_connection import DatabaseConnection
from database.insert_data import (
    insert_news_articles,
    insert_guardian_articles,
    insert_reddit_articles
)

# Load environment variables
load_dotenv()

# Set test environment
os.environ['TEST_ENV'] = 'true'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EndToEndTest(unittest.TestCase):
    """End-to-End test cases for the complete data pipeline."""

    def setUp(self):
        """Setup test environment."""
        self.db = DatabaseConnection()
        self.connection = self.db.__enter__()
        if not self.connection:
            self.skipTest("Database connection not available")

    def tearDown(self):
        """Cleanup test environment."""
        if hasattr(self, 'db'):
            self.db.__exit__(None, None, None)
            self.connection = None

    def test_trending_topics_pipeline(self):
        """Test trending topics fetching and storage."""
        try:
            # Fetch trending topics
            trending_topics = fetch_trending_topics()
            self.assertIsInstance(trending_topics, list)
            self.assertGreater(len(trending_topics), 0)
            logger.info(f"Fetched {len(trending_topics)} trending topics")
            
            # Store trending topics
            with self.connection.cursor() as cursor:
                for topic in trending_topics[:5]:  # Test with first 5 topics
                    cursor.execute("""
                        INSERT INTO api_data.trending_topics (topic, score)
                        VALUES (%s, %s)
                    """, (topic, 100))
                self.connection.commit()
        except Exception as e:
            self.fail(f"Trending topics pipeline failed: {e}")

    def test_news_pipeline(self):
        """Test news articles fetching and storage."""
        try:
            # Get keywords from trending topics
            keywords = fetch_trending_topics()[:5]
            
            # Fetch news articles
            news_articles = fetch_news(keywords)
            self.assertIsInstance(news_articles, list)
            self.assertGreater(len(news_articles), 0)
            
            # Process articles before insertion
            valid_articles = [
                {
                    'source': str(article.get('source', '')),
                    'author': str(article.get('author', '')),
                    'title': str(article.get('title')),
                    'description': str(article.get('description', '')),
                    'url': str(article.get('url')),
                    'published_at': article.get('published_at')
                }
                for article in news_articles
                if article.get('title') and article.get('url')
            ]
            
            # Insert articles
            success = insert_news_articles(self.connection, valid_articles)
            self.assertTrue(success, "Failed to insert news articles")
            logger.info(f"Inserted {len(valid_articles)} news articles")
        except Exception as e:
            self.fail(f"News pipeline failed: {e}")

    def test_guardian_pipeline(self):
        """Test Guardian articles fetching and storage."""
        try:
            # Fetch Guardian articles
            guardian_articles = fetch_guardian_data()
            self.assertIsInstance(guardian_articles, list)
            self.assertGreater(len(guardian_articles), 0)
            
            # Process articles before insertion
            valid_articles = [
                {
                    'headline': str(article.get('title', '')),
                    'url': str(article.get('url', '')),
                    'author': str(article.get('author', '')),
                    'description': str(article.get('description', '')),
                    'publication_date': article.get('published_at')
                }
                for article in guardian_articles
                if article.get('title') and article.get('url') and article.get('published_at')
            ]
            
            # Insert articles
            with self.connection.cursor() as cursor:
                for article in valid_articles:
                    cursor.execute("""
                        INSERT INTO api_data.guardian_articles 
                        (headline, url, author, description, publication_date)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (url) DO NOTHING
                    """, (
                        article['headline'],
                        article['url'],
                        article['author'],
                        article['description'],
                        article['publication_date']
                    ))
                self.connection.commit()
            logger.info(f"Inserted {len(valid_articles)} Guardian articles")
            
        except Exception as e:
            self.fail(f"Guardian pipeline failed: {e}")

    def test_reddit_pipeline(self):
        """Test Reddit data fetching and storage."""
        try:
            # Fetch Reddit data
            reddit_articles = fetch_reddit_data()
            self.assertIsInstance(reddit_articles, list)
            self.assertGreater(len(reddit_articles), 0)
            
            # Process articles before insertion
            with self.connection.cursor() as cursor:
                for article in reddit_articles:
                    if all(key in article for key in ["title", "url", "score", "created_at"]):
                        cursor.execute("""
                            INSERT INTO api_data.reddit_articles 
                            (title, url, score, created_at)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (url) DO NOTHING
                        """, (
                            str(article['title']),
                            str(article['url']),
                            int(article['score']),
                            article['created_at']
                        ))
                self.connection.commit()
            logger.info(f"Inserted {len(reddit_articles)} Reddit articles")
            
        except Exception as e:
            self.fail(f"Reddit pipeline failed: {e}")

    def test_complete_pipeline(self):
        """Test the complete data pipeline end-to-end."""
        try:
            # Get trending topics and verify
            trending_topics = fetch_trending_topics()
            self.assertIsInstance(trending_topics, list)
            self.assertGreater(len(trending_topics), 0)
            keywords = trending_topics[:5]

            # Fetch articles
            news_articles = fetch_news(keywords)
            guardian_articles = fetch_guardian_data()
            reddit_articles = fetch_reddit_data()

            # Verify fetched data
            self.assertGreater(len(news_articles), 0)
            self.assertGreater(len(guardian_articles), 0)
            self.assertGreater(len(reddit_articles), 0)

            # Insert data using single transaction
            with self.connection.cursor() as cursor:
                # Insert trending topics
                for topic in keywords:
                    try:
                        cursor.execute("""
                            INSERT INTO api_data.trending_topics (topic, score)
                            VALUES (%s, %s)
                        """, (str(topic), 100))
                    except Exception as e:
                        logger.warning(f"Failed to insert topic {topic}: {e}")
                        continue

                # Insert news articles
                for article in news_articles:
                    if article.get('title') and article.get('url'):
                        cursor.execute("""
                            INSERT INTO api_data.news_articles 
                            (source, author, title, description, url, published_at)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON CONFLICT (url) DO NOTHING
                        """, (
                            str(article.get('source', '')),
                            str(article.get('author', '')),
                            str(article.get('title')),
                            str(article.get('description', '')),
                            str(article.get('url')),
                            article.get('published_at')
                        ))

                self.connection.commit()

                # Verify data was inserted
                cursor.execute("SELECT COUNT(*) FROM api_data.news_articles")
                self.assertGreater(cursor.fetchone()[0], 0, "No news articles were inserted")

            logger.info("Complete pipeline test passed successfully")

        except Exception as e:
            self.fail(f"Complete pipeline test failed: {e}")

if __name__ == '__main__':
    unittest.main(verbosity=2)