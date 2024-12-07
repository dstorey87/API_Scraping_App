# pytrends_lib/data_cleaning.py

import logging
from nltk.sentiment import SentimentIntensityAnalyzer

def clean_data(data):
    """Standardize, validate, and clean incoming data."""
    cleaned_data = []
    sia = SentimentIntensityAnalyzer()
    for item in data:
        try:
            # Check for missing values
            if not all([item.get('title'), item.get('url'), item.get('created_utc')]):
                continue
            
            # Normalize text
            item['title'] = item['title'].strip().title()

            # Sentiment analysis
            sentiment = sia.polarity_scores(item['title'])
            item['sentiment'] = sentiment['compound']

            cleaned_data.append(item)
        except Exception as e:
            logging.error(f"Error cleaning data: {e}")
    return cleaned_data