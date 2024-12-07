import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# NewsAPI key
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Guardian API key
GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")

# Reddit API credentials
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# You can add validations to ensure keys are present
def validate_config():
    missing_vars = []
    required_vars = [
        'NEWS_API_KEY',
        'GUARDIAN_API_KEY',
        'REDDIT_CLIENT_ID',
        'REDDIT_CLIENT_SECRET',
        'REDDIT_USER_AGENT',
        'REDIRECT_URI'
    ]
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

validate_config()
