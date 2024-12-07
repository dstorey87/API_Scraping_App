# api/fetch_news_api.py

import os
import requests
import logging
import time
from dotenv import load_dotenv
from config.api_config import NEWS_API_KEY  # Ensure this points to the correct config if used

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_news(keywords, language="en", retries=3, delay=5):
    """Fetch news articles from NewsAPI, influenced by trending topics."""
    articles = []
    base_url = "https://newsapi.org/v2/everything"
    
    # Retrieve NEWS_API_KEY from environment variables
    news_api_key = os.getenv('NEWS_API_KEY')
    if not news_api_key:
        logger.error("NEWS_API_KEY is not set in the environment variables.")
        return articles  # Return empty list or handle as needed

    query = " OR ".join(keywords)
    logger.info(f"Fetching news articles with query: {query}")

    params = {
        "q": query,
        "language": language,
        "sortBy": "publishedAt",
        "pageSize": 100,
        "apiKey": news_api_key  # Pass API key as a query parameter
    }

    for attempt in range(retries):
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles", [])
            logger.info(f"Fetched {len(articles)} articles from NewsAPI.")
            return articles
        except requests.HTTPError as err:
            logger.error(f"HTTP error while fetching NewsAPI data: {err}")
        except requests.ConnectionError as err:
            logger.error(f"Connection error while fetching NewsAPI data: {err}")
        except requests.Timeout as err:
            logger.error(f"Timeout error while fetching NewsAPI data: {err}")
        except requests.RequestException as err:
            logger.error(f"Unexpected error while fetching NewsAPI data: {err}")
            break  # Non-recoverable error

        if attempt < retries - 1:
            logger.info(f"Retrying in {delay} seconds...")
            time.sleep(delay)
        else:
            logger.error("Max retries reached. Could not fetch NewsAPI data.")

    return articles  # Return empty list if all retries fail

if __name__ == "__main__":
    # Example usage
    keywords = ['technology', 'science']
    news_articles = fetch_news(keywords)
    print(f"Number of articles fetched: {len(news_articles)}")
