# services/reddit_service.py

import praw
import logging
from datetime import datetime
from database.articles_repository import ArticlesRepository
import os

logger = logging.getLogger(__name__)

class RedditService:
    SUBREDDIT_MAPPING = {
        "technology": "technology",
        "artificial intelligence": "artificial",
        "machine learning": "MachineLearning",
        "python programming": "Python"
    }

    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT")
        )
        self.db = ArticlesRepository()

    def fetch_posts(self, topic: str, time_filter: str = "day"):
        """Fetch posts from the mapped subreddit."""
        try:
            stored_posts = []
            subreddit_name = self.SUBREDDIT_MAPPING.get(topic.lower(), "technology")
            subreddit = self.reddit.subreddit(subreddit_name)

            for post in subreddit.hot(limit=10):
                article_id = self.db.insert_article(
                    title=post.title,
                    content=post.selftext,
                    source=f"reddit/r/{subreddit_name}",
                    published_date=datetime.fromtimestamp(post.created_utc)
                )
                stored_posts.append(article_id)

            logger.info(f"Fetched {len(stored_posts)} posts from r/{subreddit_name}")
            return stored_posts

        except Exception as e:
            logger.error(f"Error fetching Reddit posts from r/{subreddit_name}: {e}")
            return []