def insert_news_articles(connection, articles):
    """Insert news articles into the database."""
    cursor = connection.cursor()
    for article in articles:
        cursor.execute(
            """
            INSERT INTO api_data.news_articles (source, author, title, description, url, published_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING;
            """, (
                article.get("source", {}).get("name", "Unknown"),
                article.get("author"),
                article.get("title"),
                article.get("description"),
                article.get("url"),
                article.get("publishedAt")
            )
        )
    connection.commit()
    cursor.close()
