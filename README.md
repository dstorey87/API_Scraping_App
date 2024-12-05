# API Scraping Application

This project is designed to scrape data from various APIs and store the results in a PostgreSQL database.

## Features

- Modular API integrations for better scalability and maintainability.
- Centralized configuration for credentials and database connection settings.
- Dockerized setup for easy deployment and environment consistency.
- Integrated PyTrends support using GeneralMills/pytrends.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.10 or higher

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd API_Scraping_App
   ```

2. Set up your environment variables in the `.env` file.

3. Build and run the application:
   ```bash
   docker-compose up --build
   ```

4. Verify that the application is running and data is being inserted into the PostgreSQL database.

## PyTrends Integration

This project includes integration with GeneralMills/pytrends for fetching trending data from Google Trends.

### How to Use PyTrends
1. Update the `fetch_pytrends.py` script with your desired keywords.
2. Run the script to fetch trending data:
   ```bash
   python api/fetch_pytrends.py
   ```

3. The script outputs trending data for the past 7 days.

### Example Keywords
Modify the `keywords` list in the script:
```python
keywords = ["AI", "technology", "Python"]
```

## Contributions

Feel free to fork and submit a pull request for new features or bug fixes.

## License

This project is licensed under the MIT License.
