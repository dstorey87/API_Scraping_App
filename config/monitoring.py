# config/monitoring.py

from flask import Flask, jsonify
from database.db_connection import get_db_connection
import requests
import logging

app = Flask(__name__)

logger = logging.getLogger(__name__)

def health_check() -> dict:
    """Check system health."""
    try:
        db = get_db_connection()
        # Use %-formatting instead of f-strings
        logger.info("Health check completed: %s", str(db.status))
        return {"status": "healthy"}
    except Exception as e:
        logger.error("Health check failed: %s", str(e))
        return {"status": "unhealthy"}

@app.route('/health', methods=['GET'])
def health_check_endpoint():
    """Health check endpoint."""
    result = health_check()
    if result["status"] == "healthy":
        return jsonify(result), 200
    else:
        return jsonify(result), 500

def run_health_monitor():
    app.run(host='0.0.0.0', port=5001)

if __name__ == "__main__":
    run_health_monitor()