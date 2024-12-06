# api/fetch_news_api.py

import requests
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout
from config.api_config import NEWS_API_KEY
import time

def fetch_news(keywords, country="us", language="en", retries=3, delay=5):
    """Fetch news articles from NewsAPI, influenced by trending topics."""
    articles = []
    base_url = "https://newsapi.org/v2/everything"
    headers = {"Authorization": NEWS_API_KEY}

    # Construct the query parameter using the keywords
    query = " OR ".join(keywords)
    print(f"Fetching news articles with query: {query}")

    params = {
        "q": query,
        "language": language,
        "sortBy": "publishedAt",  # You can adjust this as needed
        "pageSize": 100  # Maximum allowed by NewsAPI per request
    }

    for attempt in range(retries):
        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles", [])
            return articles
        except (HTTPError, ConnectionError, Timeout) as err:
            print(f"Error occurred: {err}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Exiting.")
                raise
        except RequestException as err:
            print(f"Non-recoverable error: {err}")
            break

    return articles  # Return empty list if no articles fetched
