# services/analytics_service.py

import logging
import psycopg
from datetime import datetime
from database.articles_repository import ArticlesRepository

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Service for analyzing article data."""

    def __init__(self):
        """Initialize analytics service."""
        self.db = ArticlesRepository()

    def get_source_distribution(self, start_date: datetime):
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("""
                SELECT source, COUNT(*) as count
                FROM articles
                WHERE created_at >= %s
                GROUP BY source
                ORDER BY count DESC
            """, (start_date,))
            return cursor.fetchall()
        except (psycopg.Error, psycopg.DatabaseError) as e:
            logger.error("Error analyzing source distribution: %s", str(e))
            return []

    def get_topic_summary(self, topic: str, start_date: datetime):
        """Get summary of articles for a specific topic."""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("""
                SELECT source, COUNT(*) as count
                FROM articles
                WHERE title ILIKE %s
                AND created_at >= %s
                GROUP BY source
            """, (f'%{topic}%', start_date))
            return cursor.fetchall()
        except (psycopg.Error, psycopg.DatabaseError) as e:
            logger.error("Error analyzing topic summary: %s", str(e))
            return []

    def get_trend_analysis(self, topic: str, days: int = 7):
        """Analyze topic trends over time period"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("""
                SELECT DATE(created_at), COUNT(*)
                FROM articles
                WHERE title ILIKE %s
                AND created_at >= NOW() - INTERVAL %s DAY
                GROUP BY DATE(created_at)
                ORDER BY DATE(created_at)
            """, (f'%{topic}%', days))
            return cursor.fetchall()
        except (psycopg.Error, psycopg.DatabaseError) as e:
            logger.error("Error analyzing trends: %s", str(e))
            return []