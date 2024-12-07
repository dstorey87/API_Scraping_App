# API Scraping Application

This project is designed to scrape data from various APIs and store the results in a PostgreSQL database. It leverages trending data from Google Trends using PyTrends to influence the news articles fetched, ensuring the data remains relevant and timely.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Future Development Plans](#future-development-plans)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

---

## Overview

The **API Scraping App** simplifies data collection, processing, and storage by interfacing with APIs such as Google Trends, Reddit, and more. Its modular design ensures scalability, allowing easy integration of additional APIs and data pipelines.

---

## Features

- **Modular Architecture:** API integrations are modular for better scalability and maintainability.
- **Centralized Configuration:** Manages credentials and database connection settings centrally using environment variables.
- **Dockerized Setup:** Ensures easy deployment and environment consistency across different machines.
- **Integrated PyTrends Support:** Utilizes GeneralMills/pytrends to fetch and leverage trending data from Google Trends, enhancing the relevance of the scraped data.
- **Comprehensive Error Handling:** Implements robust error checking and handling across all modules to ensure reliability.
- **Automated Testing:** Includes a detailed test harness to perform end-to-end testing of all functionalities.
- **Web Dashboard:** Provides a Flask-based web interface for data visualization and admin controls.
- **CI/CD Pipeline:** Automated with GitHub Actions for testing, linting, and Docker image building.
- **Scalability:** Configured for horizontal scaling using Docker Swarm.

---

## Setup and Installation

### Prerequisites
- Python 3.10+
- Docker and Docker Compose

### Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/dstorey87/API_Scraping_App.git
   cd API_Scraping_App
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Update `.env` with your API keys and database credentials:
     ```
     POSTGRES_DB=api_scraping
     POSTGRES_USER=admin
     POSTGRES_PASSWORD=strongpassword
     POSTGRES_HOST=db
     POSTGRES_PORT=5432
     API_URL=https://api.example.com
     API_KEY=your_api_key
     ```

4. Run the application:
   ```bash
   python src/main.py
   ```

---

## Usage

1. **Run the Application:**
   ```bash
   python src/main.py
   ```

2. **Test the Modules:**
   Execute test scripts to verify functionality:
   ```bash
   pytest tests/
   ```

3. **Analyze Data:**
   Use the provided Jupyter notebook for exploratory analysis:
   ```bash
   jupyter notebook notebooks/analysis.ipynb
   ```

---

## Directory Structure

```
API_Scraping_App/
│
├── data/                     # Data storage
│   ├── raw/                  # Raw unprocessed data
│   └── processed/            # Processed and cleaned data
│
├── notebooks/                # Jupyter notebooks for analysis
│   └── analysis.ipynb
│
├── src/                      # Source code
│   ├── __init__.py
│   ├── data_ingestion.py     # Handles data fetching from APIs
│   ├── data_processing.py    # Cleans and processes data
│   └── api_client.py         # Manages API interactions
│
├── tests/                    # Unit and integration tests
│   ├── __init__.py
│   ├── test_data_ingestion.py
│   ��── test_data_processing.py
│   └── test_api_client.py
│
├── .gitignore
├── README.md                 # Project documentation
├── requirements.txt          # Dependencies
└── setup.py                  # Project setup script
```

---

## Future Development Plans

- **Expand API Support:**
  - Add more APIs such as Twitter, Facebook, and news aggregators.
  - Implement OAuth2 for APIs requiring advanced authentication.

- **Data Visualization:**
  - Integrate tools like Matplotlib or Plotly for advanced data visualization.

- **Dashboard:**
  - Build a web-based dashboard for real-time data monitoring.

- **Cloud Integration:**
  - Store processed data in cloud services like AWS S3 or Google Cloud Storage.

- **Performance Enhancements:**
  - Optimize multithreading or multiprocessing for faster data processing.

- **Machine Learning Integration:**
  - Use collected data to build predictive models for trends and insights.

---

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature/bugfix.
3. Commit your changes and push the branch.
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support

For any issues or support, please open an issue on the GitHub repository or contact the maintainer.
