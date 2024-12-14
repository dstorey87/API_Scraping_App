# services/news_api_service.py

import os
import logging
from database.articles_repository import ArticlesRepository
from api.fetch_news_api import fetch_news

logger = logging.getLogger(__name__)

class NewsAPIService:
    def __init__(self):
        self.db = ArticlesRepository()

    def fetch_articles(self, query: str):
        try:
            articles = fetch_news([query])
            stored_articles = []

            for article in articles:
                article_id = self.db.insert_article(
                    title=article['title'],
                    content=article['description'],
                    source=article['source']['name'],
                    published_date=article['publishedAt']
                )
                stored_articles.append(article_id)

            return stored_articles
        except Exception as e:
            logger.error(f"Error fetching NewsAPI articles: {e}")
            raise