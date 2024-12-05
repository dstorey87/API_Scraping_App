
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pytrends.request import TrendReq
from database.db_connection import get_db_connection

def fetch_pytrends_data(keywords):
    """Fetch trending data for given keywords using PyTrends."""
    pytrends = TrendReq(hl='en-US', tz=360)

    # Build payload for given keywords
    pytrends.build_payload(keywords, cat=0, timeframe='now 7-d', geo='', gprop='')

    # Fetch interest over time
    data = pytrends.interest_over_time()

    if not data.empty:
        data.reset_index(inplace=True)
        return data
    else:
        print("No trending data found for the given keywords.")
        return []

def main():
    # Example keywords
    keywords = ["AI", "technology", "Python"]

    # Fetch PyTrends data
    data = fetch_pytrends_data(keywords)

    if not data.empty:
        print(data)
    else:
        print("No data retrieved.")

if __name__ == "__main__":
    main()
