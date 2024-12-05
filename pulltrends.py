# PulledFriends.py
import time
from pytrends.request import TrendReq
import pandas as pd

# Documentation link for PyTrends: https://github.com/GeneralMills/pytrends

# Initialize PyTrends
pytrends = TrendReq(hl='en-US', tz=360)

# Keywords for scraping
keywords = ["Artificial Intelligence", "Machine Learning", "Technology", "AI Tools", "Tech Gadgets"]

# Function to build the payload and fetch data
def fetch_trends_data(keywords_list):
    try:
        # Building the payload
        pytrends.build_payload(
            keywords_list,
            cat=0,
            timeframe='now 7-d',  # Past 7 days
            geo='',  # Global
            gprop=''  # Web search
        )
        # Fetch interest over time
        data = pytrends.interest_over_time()

        if data.empty:
            print("No data retrieved for the given keywords.")
            return None

        # Remove 'isPartial' column if present
        if 'isPartial' in data.columns:
            data = data.drop('isPartial', axis=1)

        return data
    except Exception as e:
        print(f"Error occurred: {e}")
        time.sleep(60)  # Backoff if rate-limited
        return fetch_trends_data(keywords_list)

# Fetching data
print(f"Fetching trends for keywords: {keywords}")
trends_data = fetch_trends_data(keywords)

# Save data to CSV
if trends_data is not None:
    file_name = "google_trends_technology_ai.csv"
    trends_data.to_csv(file_name)
    print(f"Data saved successfully to {file_name}")
else:
    print("No data to save.")
