import unittest
import warnings
import logging
from api.fetch_news_api import fetch_news
from database.db_connection import get_db_connection
from database.insert_data import insert_news_articles
from pytrends_lib.trends_integration import fetch_trending_topics
from psycopg.errors import UniqueViolation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestAPIModules(unittest.TestCase):
    """Test case for API modules."""

    def test_fetch_trending_topics(self):
        """Test fetching trending topics using PyTrends."""
        # Suppress FutureWarning during the test
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=FutureWarning)
            try:
                # Fetch trending topics without providing keywords
                trending_data = fetch_trending_topics()
                # Check if the returned data is a list or a DataFrame
                data_is_valid = isinstance(trending_data, list) or not trending_data.empty
                # Assert that the data is valid
                self.assertTrue(data_is_valid, "No trending data fetched")
                logger.info("test_fetch_trending_topics passed.")
            except Exception as e:
                # Fail the test if an exception occurs
                self.fail(f"Exception occurred while fetching trending topics: {e}")

    def test_fetch_news(self):
        """Test fetching news articles from NewsAPI influenced by trending topics."""
        try:
            # Fetch news articles using the fetch_news function
            articles = fetch_news()
            # Assert that the result is a list
            self.assertIsInstance(articles, list, "Articles fetched are not in a list")
            # Assert that the list is not empty
            self.assertGreater(len(articles), 0, "No articles fetched")
            logger.info("test_fetch_news passed.")
        except Exception as e:
            # Fail the test if an exception occurs
            self.fail(f"Exception occurred while fetching news articles: {e}")

    def test_insert_news_articles(self):
        """Test inserting news articles into the database."""
        connection = get_db_connection()
        self.assertIsNotNone(connection, "Database connection should not be None")
        try:
            articles = fetch_news()
            insert_news_articles(connection, articles)
            # Additional assertions can be added here
            logger.info("test_insert_news_articles passed.")
        except Exception as e:
            self.fail(f"Exception occurred while inserting articles: {e}")
        finally:
            if connection:
                connection.close()


class TestDatabaseModules(unittest.TestCase):
    """Test case for database modules."""

    def setUp(self):
        """Set up resources before each test."""
        # Establish a database connection
        self.connection = get_db_connection()
        # Fail the test if the connection is None
        if self.connection is None:
            self.fail("Failed to connect to the database")

    def tearDown(self):
        """Clean up resources after each test."""
        # Close the database connection if it's open
        if self.connection:
            self.connection.close()

    def test_db_connection(self):
        """Test that the database connection is successful."""
        # Assert that the connection is not None
        self.assertIsNotNone(self.connection, "Database connection failed")

    def test_insert_news_articles(self):
        """Test inserting news articles into the database."""
        try:
            # Fetch news articles
            articles = fetch_news()
            # Insert news articles into the database
            insert_news_articles(self.connection, articles)
            # If no exception is raised, the test passes
            self.assertTrue(True, "Articles inserted successfully")
        except UniqueViolation as uv:
            # Handle unique constraint violations (e.g., duplicate URLs)
            self.fail(f"UniqueViolation error occurred: {uv}")
        except Exception as e:
            # Fail the test if any other exception occurs
            self.fail(f"Failed to insert articles: {e}")


class TestEndToEnd(unittest.TestCase):
    """End-to-End test case for the entire data flow."""

    def test_full_data_flow(self):
        # Obtain or define test keywords
        test_keywords = ["test", "api", "news"]
        articles = fetch_news(keywords=test_keywords)
        try:
            # Fetch trending topics
            trending_data = fetch_trending_topics()
            self.assertTrue(
                isinstance(trending_data, list) or not trending_data.empty,
                "Trending data is invalid"
            )

            # Fetch news articles influenced by trending topics
            articles = fetch_news()
            self.assertIsInstance(articles, list, "Articles fetched are not in a list")
            self.assertGreater(len(articles), 0, "No articles fetched")

            # Establish a database connection
            connection = get_db_connection()
            self.assertIsNotNone(connection, "Failed to connect to the database")

            try:
                # Insert news articles into the database
                insert_news_articles(connection, articles)
                self.assertTrue(True, "Articles inserted successfully")
            finally:
                # Close the database connection
                connection.close()

        except Exception as e:
            # Fail the test if any exception occurs during the full data flow
            self.fail(f"End-to-End data flow test failed: {e}")


if __name__ == "__main__":
    # Run the test cases
    unittest.main()