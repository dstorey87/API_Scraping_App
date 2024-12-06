import psycopg
from psycopg import sql
from psycopg.errors import UniqueViolation


def insert_news_articles(connection, articles):
    """Insert news articles into the database."""
    if connection is None:
        print("No database connection available.")
        return

    try:
        with connection.cursor() as cursor:
            for article in articles:
                # Data validation: Ensure required fields are present
                title = article.get("title")
                url = article.get("url")
                if not title or not url:
                    print("Article missing required fields. Skipping.")
                    continue

                # Prepare SQL query using psycopg's sql module for safety
                insert_query = sql.SQL("""
                    INSERT INTO api_data.news_articles (source, author, title, description, url, published_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (url) DO NOTHING;
                """)

                try:
                    # Execute query with provided parameters
                    cursor.execute(
                        insert_query, (
                            article.get("source", {}).get("name", "Unknown"),
                            article.get("author"),
                            title,
                            article.get("description"),
                            url,
                            article.get("publishedAt")
                        )
                    )
                except UniqueViolation:
                    # Handle unique constraint violations (e.g., duplicate URLs)
                    print(f"Duplicate entry detected for URL: {url}. Skipping insertion.")
            # Commit the transaction after all insertions
            connection.commit()
            print("All articles inserted successfully.")
    except Exception as e:
        # Print an error message and roll back the transaction if an error occurs
        print(f"Error inserting articles: {e}")
        connection.rollback()
