import requests
from config.api_config import NEWS_API_KEY

def fetch_news():
    """Fetch news articles from NewsAPI."""
    BASE_URL = "https://newsapi.org/v2/top-headlines"
    PARAMS = {
        "country": "us",
        "language": "en",
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(BASE_URL, params=PARAMS)
    response.raise_for_status()
    return response.json().get("articles", [])
