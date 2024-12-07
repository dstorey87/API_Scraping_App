# web_interface.py

from flask import Flask, render_template, request, redirect, url_for
from database.db_connection import get_db_connection
from pytrends_lib.data_cleaning import clean_data
import logging

app = Flask(__name__)

@app.route('/')
def index():
    connection = get_db_connection()
    trending_topics = connection.execute('SELECT * FROM trending_topics').fetchall()
    news_articles = connection.execute('SELECT * FROM news_articles').fetchall()
    connection.close()
    return render_template('index.html', trending=trending_topics, articles=news_articles)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Logic to control scraping schedules or trigger scraping
        pass
    connection = get_db_connection()
    logs = connection.execute('SELECT * FROM logs').fetchall()
    connection.close()
    return render_template('admin.html', logs=logs)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)