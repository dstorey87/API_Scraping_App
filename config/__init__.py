import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv('MODEL_NAME', 'codellama/code-llama-small')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', '5672'))
