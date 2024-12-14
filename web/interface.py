# interface.py

from flask import Flask, render_template, Blueprint
import logging
import os

from services.analytics_service import AnalyticsService
from services.visualization_service import VisualizationService

logger = logging.getLogger(__name__)

web_bp = Blueprint('web', __name__)

def create_app():
    """Create and configure Flask application."""
    # Create reports directory inside web/static
    reports_dir = os.path.join(os.path.dirname(__file__), 'static', 'reports')
    os.makedirs(reports_dir, exist_ok=True)

    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), 'static'))

    app.register_blueprint(web_bp)

    @app.route('/')
    def index():
        """Display the main dashboard."""
        reports = {
            'Overall Distribution': 'source_distribution.html',
            'Technology': 'topic_technology.html',
            'Artificial Intelligence': 'topic_artificial_intelligence.html',
            'Machine Learning': 'topic_machine_learning.html',
            'Python Programming': 'topic_python_programming.html'
        }
        return render_template('index.html', reports=reports)

    return app

if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(debug=True)