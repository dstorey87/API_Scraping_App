# api/__init__.py

from .fetch_guardian_api import fetch_guardian_data
from .fetch_news_api import fetch_news
from .fetch_pytrends import fetch_trending_topics
from .fetch_reddit_data import fetch_reddit_data
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    trending_topics = fetch_trending_topics()
    print(f"Trending topics: {trending_topics}")