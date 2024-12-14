"""Service for interacting with The Guardian's API."""
from datetime import datetime
import logging
import os
from typing import List, Optional

import requests
from requests.exceptions import RequestException

from database.articles_repository import ArticlesRepository

logger = logging.getLogger(__name__)

class GuardianService:
    """Handles interactions with The Guardian's API and article storage."""

    def __init__(self) -> None:
        """Initialize Guardian service with API configuration."""
        self.api_key = os.getenv("GUARDIAN_API_KEY")
        if not self.api_key:
            raise ValueError("GUARDIAN_API_KEY environment variable not set")

        self.base_url = "https://content.guardianapis.com/search"
        self.db = ArticlesRepository()

    def fetch_articles(self, query: str, from_date: Optional[str] = None) -> List[int]:
        """
        Fetch articles from The Guardian API matching the given query.

        Args:
            query: Search term to query articles
            from_date: Optional date filter in YYYY-MM-DD format

        Returns:
            List of stored article IDs

        Raises:
            RequestException: If API request fails
            ValueError: If response format is invalid
        """
        params = {
            'api-key': self.api_key,
            'q': query,
            'show-fields': 'all',
            'page-size': 50
        }

        if from_date:
            params['from-date'] = from_date

        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            if 'response' not in data or 'results' not in data['response']:
                raise ValueError("Invalid API response format")

            stored_articles = []
            for article in data['response']['results']:
                article_id = self.db.insert_guardian_article(
                    title=article['webTitle'],
                    url=article['webUrl'],
                    publication_date=datetime.strptime(
                        article['webPublicationDate'],
                        '%Y-%m-%dT%H:%M:%SZ'
                    )
                )
                stored_articles.append(article_id)

            logger.info(
                "Successfully fetched and stored %d articles",
                len(stored_articles)
            )
            return stored_articles

        except RequestException as e:
            logger.error("API request failed: %s", e)
            raise
        except (KeyError, ValueError) as e:
            logger.error("Error processing response: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            raise