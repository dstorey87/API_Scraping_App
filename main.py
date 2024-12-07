# main.py

import time
from api import fetch_news_api
from pytrends_lib import trends_integration
from database import db_connection, setup_main_db, insert_data

def main():
    max_iterations = 5  # Set the maximum number of iterations
    iteration = 0

    while iteration < max_iterations:
        print(f"Starting iteration {iteration + 1}/{max_iterations}")

        # Fetch trending searches
        trending_searches = trends_integration.fetch_trending_topics()
        print(f"Trending keywords: {trending_searches}")

        # Fetch news articles based on trending searches
        news_articles = fetch_news_api.fetch_news(trending_searches)
        print(f"Fetched {len(news_articles)} articles from NewsAPI.")

        # Insert news articles into the database
        db_conn = db_connection.get_db_connection()
        if db_conn:
            setup_main_db.setup_schema(db_conn)
            insert_data.insert_news_articles(db_conn, news_articles)
            db_connection.close_db_connection(db_conn)
            print("News articles inserted successfully!")

        # Increment the iteration counter
        iteration += 1

        # Sleep for a while before the next iteration (optional)
        time.sleep(60)  # Sleep for 60 seconds

    print("Completed all iterations. Exiting...")

if __name__ == "__main__":
    main()
