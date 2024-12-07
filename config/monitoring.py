# config/monitoring.py

from flask import Flask, jsonify
from database.db_connection import get_db_connection
import requests
import logging

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        # Check database connection
        connection = get_db_connection()
        connection.close()
        
        # Check external API
        response = requests.get('https://www.reddit.com/', timeout=5)
        if response.status_code != 200:
            raise Exception("Reddit API is unreachable.")
        
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

def run_health_monitor():
    app.run(host='0.0.0.0', port=5001)

if __name__ == "__main__":
    run_health_monitor()