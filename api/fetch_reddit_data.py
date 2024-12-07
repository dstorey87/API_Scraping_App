# api/fetch_reddit_data.py

import praw
import logging
from database.db_connection import get_db_connection
from database.insert_data import insert_reddit_articles
from config.api_config import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT
)
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

def fetch_reddit_data():
    """Fetch trending topics and posts from Reddit."""
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        subreddit = reddit.subreddit('all')
        trending_posts = []
        for post in subreddit.hot(limit=10):
            trending_posts.append({
                "title": post.title,
                "score": post.score,
                "url": post.url,
                "created_at": datetime.fromtimestamp(post.created_utc)  # Convert to datetime
            })
        connection = get_db_connection()
        if connection:
            insert_reddit_articles(connection, trending_posts)
            connection.close()
        return trending_posts
    except Exception as e:
        logging.error(f"Error fetching Reddit data: {e}")
        return None

if __name__ == "__main__":
    fetch_reddit_data()