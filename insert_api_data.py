import psycopg
import requests

# Step 1: Connect to PostgreSQL using Psycopg 3
with psycopg.connect(
    dbname="main_db",
    user="admin",
    password="strongpassword",
    host="localhost",
    port=5432
) as connection:
    # Create a cursor for executing queries
    with connection.cursor() as cursor:

        # Step 2: Fetch Data from the API
        response = requests.get("https://jsonplaceholder.typicode.com/posts")
        data = response.json()

        # Step 3: Insert Data into PostgreSQL
        for item in data:
            cursor.execute(
                """
                INSERT INTO api_data.jsonplaceholder_data (id, title, body)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (item['id'], item['title'], item['body'])
            )
        
        # Commit changes
        connection.commit()

print("Data inserted successfully!")
