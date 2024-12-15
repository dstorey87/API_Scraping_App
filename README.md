# Local LLM Integration with LangChain

This project implements LangChain functionality with local Large Language Models (LLMs) using PyTorch and CUDA acceleration.

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

The **LangChain Integration Application** simplifies the development of AI-powered applications by integrating LangChain functionality with various AI models and chain types. Its modular design ensures scalability, allowing easy integration of additional AI models and chain types.

---

## Features

- **Local LLM Integration:** Run models locally with PyTorch
- **CUDA Acceleration:** GPU-optimized inference
- **Modular Architecture:** Separate services for different chain types
- **Worker System:** Distributed task processing for AI operations
- **Testing Framework:** Complete test coverage

---

## Setup and Installation

### Prerequisites
- Python 3.11+
- CUDA capable GPU
- PyTorch with CUDA support
- Virtual Environment

### Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/dstorey87/LangChain_Integration_App.git
   cd LangChain_Integration_App
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
     OPENAI_API_KEY=your_openai_api_key
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
project/
├── ai_workers/                 # Distributed worker system
├── api/                        # API functionalities
├── config/                     # Configuration files
├── cuda/                       # CUDA-related functionalities
├── database/                   # Database schemas and migrations
├── langchain_service/          # Service layer for LLMs
├── pytorch/                    # PyTorch models and scripts
├── pytrends_lib/               # Library for Google Trends data
├── pytrends_tool/              # Tool for interacting with pytrends
├── services/                   # Background services and workers
├── utils/                      # Utility scripts and helper functions
├── web/                        # Web interface code
│   └── interface.py            # Flask web application
├── templates/                  # HTML templates
│   └── index.html              # Main dashboard template
├── static/                     # Static files
│   └── reports/                # Generated reports
└── tests/                      # Test suite
```

---

## Future Development Plans

# Project Plan for Local LLM Integration with LangChain

## Overview
This document outlines the steps necessary to complete the API Scraping Application. The project aims to scrape data from various APIs, process the results, and store them in a PostgreSQL database. The application leverages Google Trends data to guide content relevance. The plan is divided into phases to facilitate modular, incremental development and deployment.

## Phase 1: Core Functionality Implementation

### 1. LangChain Integration with Local LLMs
- **Base Setup**: Implement core LangChain functionality in the `o1_langchain_integration` directory.
  - **Implementation**:
    - Set up local LLM models using PyTorch
    - Configure LangChain for local model usage
    - Implement basic chain types with local models
  - **Status**: In Progress

### 2. Service Layer
- **LangChain Service**: Create modular service layer in `langchain_service` directory.
  - **Implementation**:
    - Set up service structure for different chain types
    - Implement CUDA acceleration support
    - Add error handling and logging
  - **Status**: Pending

### 3. AI Workers
- **Worker Implementation**: Create specialized AI workers in `ai_workers` directory.
  - **Implementation**:
    - Set up worker queue system for distributed model inference
    - Implement GPU-based task distribution
    - Add monitoring and logging
  - **Status**: Pending

### 4. CUDA Integration
- **GPU Acceleration**: Optimize LLM performance using CUDA.
  - **Implementation**:
    - Configure CUDA environment ([cuda.ps1](cuda.ps1))
    - Set up PyTorch with CUDA support
    - Implement model quantization
  - **Status**: In Progress

### 4. API Integrations
- **Reddit Integration**: Extend the current API capabilities by integrating with the Reddit API. Focus on scraping trending topics from relevant subreddits.
  - **Implementation**:
    - Created `fetch_reddit_data.py` to collect and structure Reddit data.
    - Used the `PRAW` library to interact with Reddit's API.
    - Stored results in a new table named `reddit_articles`.
  - **Status**: **Complete**

- **Guardian News API**: Add integration with the Guardian API to enhance the scope of news coverage.
  - **Implementation**:
    - Created `fetch_guardian_api.py` to fetch articles from the Guardian API.
    - Parsed JSON responses and extracted necessary information (headline, URL, publication date).
    - Stored fetched articles in the `guardian_articles` table.
  - **Status**: **Complete**

- **PyTrends Enhancement**: Expand on the current PyTrends integration.
  - **Implementation**:
    - Modified `fetch_pytrends.py` to allow dynamic updating of trending topics at regular intervals.
    - Scheduled PyTrends scraping tasks via a cron job to ensure relevance.
    - Stored trending topics in the PostgreSQL database for historical analysis.
  - **Status**: **Complete**

### 5. Database Improvements
- **Database Design Review**: Refactor the database schema to accommodate new API sources.
  - **Implementation**:
    - Created tables for `reddit_articles`, `guardian_articles`, and other relevant data sources.
    - Added necessary relationships and indexes to improve query performance.
  - **Status**: **Complete**

- **Centralized Connection Management**: Enhance the `get_db_connection` function to include retry logic and better connection pooling, optimizing performance and reducing downtime.
  - **Implementation**:
    - Enhanced `db_connection.py` to include retry logic and connection pooling.
    - Implemented centralized connection management for all database interactions.
  - **Status**: **Complete**

## Phase 2: Data Processing and Quality Control

### 1. Data Cleaning and Transformation
- **Data Cleaning Module**: Implement a module (`data_cleaning.py`) that standardizes, validates, and cleans incoming data before inserting it into the database.
  - Address data consistency by ensuring field formats match the database schema.
  - Use Llama 3.2 Vision for sentiment analysis and keyword extraction.

### 2. Error Handling Improvements
- **Unified Error Logging**: Implement centralized logging using Python's `logging` library.
  - Configure logs to store in a dedicated `logs/` directory for easy debugging.
  - Ensure all API integrations have robust error handling and write detailed log messages for any failures.

### 3. Monitoring and Alerts
- **Health Check**: Implement an automatic health check endpoint (`/health`) to verify all API and database connections are functional.
- **Error Alerts**: Set up email or Slack notifications for critical errors using services like SMTP or webhook integrations.

## Phase 3: Deployment Enhancements

### 1. Docker Optimization
- **Dockerfile and Docker Compose Improvements**: Optimize the Docker configuration to reduce image size and improve build caching.
  - Ensure all dependencies are installed using a multi-stage Dockerfile to keep the production image lean.
  - Create a `.env.sample` file to serve as a template for environment configuration.

- **Service Configuration**: Refine the `docker-compose.yml` to add restart policies, ensuring services automatically restart on failure.

### 2. Deployment Automation
- **CI/CD Setup**: Set up GitHub Actions to automate testing, linting, and building Docker images.
  - Include steps to run unit tests from `test_harness.py` and deploy to a test environment.

### 3. Scalability Considerations
- **Database Sharding**: Assess the need for database sharding or read replicas to manage increased data volume as more APIs are integrated.
- **Horizontal Scaling for Scraping**: Implement scaling mechanisms using Docker Swarm or Kubernetes to handle multiple scraping tasks concurrently without service interruption.

## Phase 4: User Interface Development

### 1. Web Dashboard
- **Basic Frontend with Flask**: Create a simple Flask web interface (`web_interface.py`) to display the collected data.
  - Users can view trending topics, news articles, and manage data sources.

- **Admin Controls**: Provide an admin panel to control scraping schedules, view logs, and restart scraping jobs when needed.

## Documentation and Knowledge Sharing
- **Documentation Updates**: Maintain up-to-date documentation for every new integration, stored in the `docs/` directory.
  - Update the `README.md` with setup instructions for each phase as features are added.

- **Tutorials and Guides**: Create beginner-friendly `.md` files for major modules (e.g., `pytrends_integration.md`, `reddit_integration.md`) to help understand the functionality and setup.

## Timeline and Milestones
- **Week 1**: Complete Reddit and Guardian API integrations.
- **Week 2**: Database improvements and data cleaning module.
- **Week 3**: Enhance error handling and add logging/monitoring features.
- **Week 4**: Optimize Docker and automate deployment.
- **Week 5**: Develop and deploy the web dashboard.

## Key Goals
- **Modular Development**: Ensure each feature is modular and easily extensible.
- **Beginner-Friendly Documentation**: Tailor all documentation for novice developers, providing comprehensive guides.
- **Focus on Scalability**: Implement features with an eye towards scaling to handle larger volumes of data.

## Next Steps
- Review current `main.py` and existing integrations for refactoring opportunities.
- Start with implementing the Reddit API integration.
- Update the `project_plan.md` weekly with completed milestones and new priorities.


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
