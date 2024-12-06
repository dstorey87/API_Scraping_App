# API Scraping Application

This project is designed to scrape data from various APIs and store the results in a PostgreSQL database. It leverages trending data from Google Trends using PyTrends to influence the news articles fetched, ensuring the data remains relevant and timely.

## Features

- **Modular Architecture:** API integrations are modular for better scalability and maintainability.
- **Centralized Configuration:** Manages credentials and database connection settings centrally using environment variables.
- **Dockerized Setup:** Ensures easy deployment and environment consistency across different machines.
- **Integrated PyTrends Support:** Utilizes GeneralMills/pytrends to fetch and leverage trending data from Google Trends, enhancing the relevance of the scraped data.
- **Comprehensive Error Handling:** Implements robust error checking and handling across all modules to ensure reliability.
- **Automated Testing:** Includes a detailed test harness to perform end-to-end testing of all functionalities.

## Prerequisites

- **Docker and Docker Compose:** Ensure Docker is installed and properly configured on your machine.
- **Python 3.10 or Higher:** Required for local development and testing.
- **PostgreSQL Database:** The application stores scraped data in a PostgreSQL database.

## Getting Started

### 1. Clone the Repository

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
