# api/fetch_guardian_api.py

import logging
from database.db_connection import get_db_connection
from database.insert_data import insert_guardian_articles
from config.api_config import GUARDIAN_API_KEY
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_guardian_data():
    """Fetch data from the Guardian API."""
    try:
        connection = get_db_connection()
        if connection is None:
            logger.error("Database connection failed.")
            return None
        
        url = "https://content.guardianapis.com/search"
        params = {
            'api-key': GUARDIAN_API_KEY,
            'show-fields': 'all',
            'page-size': 10
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        articles = []
        for result in data.get('response', {}).get('results', []):
            article = {
                "source": "Guardian",
                "author": result.get("fields", {}).get("byline"),
                "title": result.get("webTitle"),
                "description": result.get("fields", {}).get("trailText"),
                "url": result.get("webUrl"),
                "published_at": result.get("webPublicationDate")
            }
            if all(article.values()):
                articles.append(article)
            else:
                logger.warning("Guardian article missing required fields. Skipping.")

        insert_guardian_articles(connection, articles)
        logger.info("Guardian data fetched and inserted successfully.")
        return articles
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as e:
        logger.error(f"Error fetching Guardian data: {e}")
    return None

if __name__ == "__main__":
    fetch_guardian_data()