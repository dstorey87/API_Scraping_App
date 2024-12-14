# services/sentiment_service.py

from transformers import pipeline

class SentimentService:
    def __init__(self):
        self.analyzer = pipeline('sentiment-analysis')

    def analyze_sentiment(self, text: str):
        return self.analyzer(text)[0]