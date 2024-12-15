from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

load_dotenv()
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')
if not HUGGINGFACE_TOKEN:
    logger.error("HUGGINGFACE_TOKEN not found in environment")
    raise ValueError("HUGGINGFACE_TOKEN not found in .env file")