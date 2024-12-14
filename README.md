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

- **Expand AI Model Support:**
  - Add more AI models such as GPT-4, BERT, and other NLP models.
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
