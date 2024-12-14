# GitHub Copilot Guide for API Scraping Application

## Overview
This guide provides instructions for GitHub Copilot to automate coding tasks for each core functionality described in our `project_plan.md`. The document outlines detailed steps, expectations, and goals for each development phase, ensuring that Copilot can efficiently contribute to our API Scraping Application.

## Phase 1: Core Functionality Implementation

### 1. Reddit API Integration
- **File Creation**: Create a Python script named `fetch_reddit_data.py` within the `api/` directory.
- **Goal**: Fetch trending topics and posts from Reddit.
- **Instructions**:
  - Use the `PRAW` library to interact with Reddit's API, and ensure the script retrieves relevant subreddits based on topics of interest (e.g., `technology`, `news`).
  - Add functionality to filter posts based on upvotes and recency to prioritize relevance.
  - Store the data in a new table called `reddit_articles` in the PostgreSQL database.
  - Ensure the database connection uses our centralized `get_db_connection()` function.
  - Include retry logic and appropriate error handling for failed API requests.

### 2. Guardian News API Integration
- **File Creation**: Create `fetch_guardian_api.py` within the `api/` directory.
- **Goal**: Integrate the Guardian News API to pull articles on trending topics.
- **Instructions**:
  - Use the `requests` library to interact with the Guardian News API.
  - Accept trending keywords as input and fetch related articles.
  - Parse JSON responses, extract necessary information (headline, URL, publication date), and insert them into a new table called `guardian_articles`.
  - Use the `insert_data.py` function from the `database/` directory for insertion.
  - Add error logging and fallback mechanisms to ensure reliability.

### 3. PyTrends Enhancement
- **File Update**: Modify `pytrends_tool/fetch_trending_topics.py`.
- **Goal**: Automate regular updates for trending topics.
- **Instructions**:
  - Expand the existing function to allow dynamic scheduling of topic retrieval every 24 hours.
  - Store trending topics in the PostgreSQL database for historical analysis.
  - Create a scheduling mechanism using the `schedule` library or a simple cron job.
  - Ensure to validate trending topics before storage to prevent duplicates.

## Phase 2: Data Processing and Quality Control

### 1. Data Cleaning Module
- **File Creation**: Create `data_cleaning.py` in the `pytrends_lib/` directory.
- **Goal**: Standardize, validate, and clean incoming data before inserting it into the database.
- **Instructions**:
  - Create functions to check for missing values and standardize data formats (e.g., dates, text normalization).
  - Leverage Llama 3.2 Vision for sentiment analysis and keyword extraction.
  - Integrate the data cleaning step within the `main.py` workflow to ensure clean data is inserted.
  - Implement error handling for incompatible data types.

### 2. Unified Error Handling and Logging
- **File Update**: Modify `config/error_logging.py`.
- **Goal**: Implement centralized logging and error handling.
- **Instructions**:
  - Update the `get_db_connection()` function to add retry logic in case of connection failures.
  - Use Python's `logging` library to create loggers for each core module (`api`, `database`, etc.).
  - Ensure log files are saved in the `logs/` directory with meaningful error messages.
  - Add context to logs so that every error trace contains information about the affected module and function.

### 3. Monitoring and Alerts
- **File Creation**: Create `monitoring.py` in the `config/` directory.
- **Goal**: Automate health checks and set up error alerts.
- **Instructions**:
  - Create a health check endpoint (`/health`) using Flask that returns the status of API connections and database health.
  - Use the `smtplib` library or webhooks to send email/Slack notifications for any critical error.
  - Schedule regular checks and integrate with the main application.

## Phase 3: Deployment Enhancements

### 1. Docker Optimization
- **File Update**: Modify `Dockerfile` and `docker-compose.yml`.
- **Goal**: Optimize Docker for smaller image size and quicker builds.
- **Instructions**:
  - Convert the Dockerfile into a multi-stage build to separate dependencies, tests, and the final production image.
  - Update `docker-compose.yml` to include service restart policies for all core services.
  - Create an `.env.sample` file to guide developers on setting up their environment variables.
  - Implement volume persistence for PostgreSQL data to prevent data loss during container rebuilds.

### 2. CI/CD Setup
- **File Creation**: Create `.github/workflows/main.yml`.
- **Goal**: Automate testing, linting, and Docker image building.
- **Instructions**:
  - Use GitHub Actions to automate the CI/CD pipeline.
  - Include jobs for linting (`flake8`), running unit tests (`pytest`), and building Docker images.
  - Set up environment variables and secrets for running tests safely without exposing credentials.

### 3. Scalability Considerations
- **File Update**: Modify `docker-compose.yml`.
- **Goal**: Prepare for horizontal scaling.
- **Instructions**:
  - Implement Docker Swarm for scaling scraping tasks and services.
  - Ensure the PostgreSQL service can accommodate read replicas if necessary.
  - Include configurations for scaling scraping workers based on data volume.

## Phase 4: User Interface Development

### 1. Web Dashboard
- **File Creation**: Create `web_interface.py` using Flask.
- **Goal**: Develop a web UI for data visualization.
- **Instructions**:
  - Set up a basic Flask web server in `web_interface.py`.
  - Create routes to view trending topics, scraped articles, and logs.
  - Add pagination for articles and trending topics.
  - Ensure the dashboard is accessible via port `5000` and integrate it into the `docker-compose.yml` file.

### 2. Admin Controls
- **File Update**: Extend `web_interface.py` to include admin capabilities.
- **Goal**: Allow admins to control scraping and view logs.
- **Instructions**:
  - Add a `/admin` route to manage scraping schedules and view error logs.
  - Allow functionality to manually trigger scraping for any data source.
  - Add authentication to the admin panel to restrict access.

## General Guidelines for Copilot
- **Modular Approach**: Keep code modular by creating separate files for each functionality.
- **Documentation**: Generate docstrings for every function, including examples of expected inputs and outputs.
- **Error Handling**: Always add error handling, including retries and fallback mechanisms for critical functions.
- **Logs and Alerts**: Ensure every new feature logs its progress and any errors, using the centralized logging setup.
- **Refactoring Opportunities**: When modifying existing code, always refactor for better readability and reusability.

## Conclusion
This guide is intended to ensure Copilot can effectively contribute to each phase of development. Follow the structured steps, keep the implementation aligned with our goals, and log progress regularly to ensure quality and consistency. Regularly update this guide as new features and phases are introduced.

# GitHub Copilot Guide for LangChain Integration

## Phase 1: Core Implementation

### 1. LangChain Setup
- **File Creation**: Set up core files in `o1_langchain_integration/`
- **Goal**: Implement basic LangChain functionality
- **Instructions**:
  - Create base chain types
  - Set up OpenAI integration
  - Implement proper error handling
  - Add logging and monitoring

### 2. Service Layer Implementation
- **File Creation**: Develop services in `langchain_service/`
- **Goal**: Create modular service layer
- **Instructions**:
  - Implement service classes for different chain types
  - Add connection management
  - Set up error handling and retries

[Rest of structure remains similar but focused on LangChain...]

## 3. [GitHubCopilot.md](GitHubCopilot.md) Updates:
