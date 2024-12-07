import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Primary Database configuration dictionary
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")
}

# Admin Database configuration
ADMIN_DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_ADMIN_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")
}

# Validate Environment Variables
required_vars = [
    "POSTGRES_DB",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_ADMIN_DB"
]

missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    missing = ", ".join(missing_vars)
    raise EnvironmentError(f"Missing required environment variables: {missing}")
