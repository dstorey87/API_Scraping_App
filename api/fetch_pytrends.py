# api/fetch_pytrends.py

from pytrends.request import TrendReq
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_trending_topics():
    """Fetch trending topics using PyTrends."""
    pytrends = TrendReq(hl='en-US', tz=360)
    trending_searches_df = pytrends.trending_searches(pn='united_states')
    trending_searches = trending_searches_df[0].tolist()
    logger.info(f"Fetched trending searches: {trending_searches}")
    return trending_searches