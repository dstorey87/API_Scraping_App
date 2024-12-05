from pytrends.request import TrendReq

def fetch_trending_topics(keywords):
    """Fetch trending data for given keywords using GeneralMills/pytrends."""
    pytrends = TrendReq(hl='en-US', tz=360)

    # Build payload with keywords
    pytrends.build_payload(keywords, cat=0, timeframe='now 7-d', geo='', gprop='')

    # Fetch interest over time
    data = pytrends.interest_over_time()

    if not data.empty:
        data = data.reset_index()
        return data
    else:
        print("No trending data found for the given keywords.")
        return []
