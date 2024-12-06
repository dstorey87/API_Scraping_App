from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
import time
import logging
import re
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def sanitize_keyword(keyword):
    """Remove special characters from keywords."""
    return re.sub(r'[^\w\s]', '', keyword)

def fetch_trending_topics(keywords=None, retries=3, delay=5, batch_size=5):
    """Fetch trending data for given keywords using PyTrends."""
    pytrends = TrendReq(hl='en-US', tz=360)
    
    if keywords is None:
        trending_searches_df = pytrends.trending_searches(pn='united_states')
        keywords = trending_searches_df[0].tolist()
        logger.info(f"Fetched trending searches: {keywords}")
    
    if not keywords:
        logger.warning("No keywords available to fetch trending topics.")
        return []
    
    # Sanitize keywords
    keywords = [sanitize_keyword(kw) for kw in keywords if sanitize_keyword(kw)]
    
    # Split keywords into batches
    for i in range(0, len(keywords), batch_size):
        batch = keywords[i:i + batch_size]
        attempt = 0
        while attempt < retries:
            try:
                logger.info(f"Attempt {attempt + 1}: Building payload with keywords: {batch}")
                pytrends.build_payload(
                    kw_list=batch,
                    cat=0,
                    timeframe='now 7-d',
                    geo='US',
                    gprop=''
                )
                logger.info("Fetching interest over time data...")
                data = pytrends.interest_over_time()
                if not data.empty:
                    data = data.reset_index()
                    data = data.infer_objects(copy=False)
                    logger.info("Trending data fetched successfully.")
                    return data
                else:
                    logger.warning("No trending data found for the given keywords.")
                    return []
            except ResponseError as e:
                logger.error(f"Response error: {e}")
                backoff_time = delay * (2 ** attempt)
                logger.info(f"Retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)
                attempt += 1
            except ValueError as ve:
                logger.error(f"Value error: {ve}")
                return []
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                return []
        logger.error("Max retries reached for current batch. Moving to next batch.")
    return []
