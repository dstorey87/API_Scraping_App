# database/articles_repository.py

from datetime import datetime
from database.db_connection import get_db_connection
import logging

logger = logging.getLogger(__name__)

class ArticlesRepository:
    def __init__(self):
        self.connection = get_db_connection()

    def insert_article(self, title: str, content: str, source: str, published_date: datetime = None):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO articles (title, content, source, published_date)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (title, content, source, published_date))
            article_id = cursor.fetchone()[0]
            self.connection.commit()
            return article_id
        except Exception as e:
            logger.error(f"Error inserting article: {e}")
            self.connection.rollback()
            raise

    def insert_guardian_article(self, title: str, url: str, publication_date: datetime):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO guardian_articles (title, url, publication_date)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (title, url, publication_date))
            article_id = cursor.fetchone()[0]
            self.connection.commit()
            return article_id
        except Exception as e:
            logger.error(f"Error inserting guardian article: {e}")
            self.connection.rollback()
            raise

    def __del__(self):
        if hasattr(self, 'connection'):
            self.connection.close()