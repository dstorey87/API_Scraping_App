from api.fetch_news_api import fetch_news
from database.db_connection import get_db_connection
from database.insert_data import insert_news_articles

def main():
    # Fetch news articles
    articles = fetch_news()

    # Insert data into the database
    connection = get_db_connection()
    try:
        insert_news_articles(connection, articles)
        print("News articles inserted successfully!")
    finally:
        connection.close()

if __name__ == "__main__":
    main()
