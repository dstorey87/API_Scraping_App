# main.py

from api.fetch_news_api import fetch_news
from database.db_connection import get_db_connection
from database.insert_data import insert_news_articles
from pytrends_lib.trends_integration import fetch_trending_topics
from database.setup_main_db import setup_database  # Import the setup_database function


def main():
    """Main function to fetch news articles and insert them into the database."""
    # Set up the database (create database, schema, and tables if they don't exist)
    setup_database()

    connection = None
    try:
        # Fetch trending topics
        trending_data = fetch_trending_topics()
        
        # Extract trending keywords
        if trending_data is not None and not trending_data.empty:
            trending_keywords = trending_data.columns.tolist()
            print(f"Trending keywords: {trending_keywords}")
        else:
            trending_keywords = ["technology", "business"]  # Default keywords if fetching fails
            print("Using default keywords for news fetching.")

        # Fetch news articles influenced by trending topics
        articles = fetch_news(keywords=trending_keywords)
        print(f"Fetched {len(articles)} articles from NewsAPI.")

        # Establish a database connection
        connection = get_db_connection()
        if connection is None:
            print("Failed to connect to the database. Exiting application.")
            return

        # Insert news articles into the database
        insert_news_articles(connection, articles)
        print("News articles inserted successfully!")

    except Exception as e:
        print(f"An unexpected error occurred in the main application: {e}")
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()
