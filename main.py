# main.py

import logging
import os
import time
from datetime import datetime, timedelta
from dataclasses import dataclass
from flask import Flask

from services.guardian_service import GuardianService
from services.news_api_service import NewsAPIService
from services.reddit_service import RedditService
from services.analytics_service import AnalyticsService
from services.visualization_service import VisualizationService
from web.interface import create_app

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

@dataclass
class NewsServices:
    """Container for news-related services."""
    guardian: GuardianService
    news_api: NewsAPIService
    reddit: RedditService
    analytics: AnalyticsService
    visualization: VisualizationService

def initialize_services() -> NewsServices:
    """Initialize all required services."""
    return NewsServices(
        guardian=GuardianService(),
        news_api=NewsAPIService(),
        reddit=RedditService(),
        analytics=AnalyticsService(),
        visualization=VisualizationService()
    )

def process_articles(services: NewsServices, topic: str, date: str) -> None:
    """Process articles for a given topic."""
    logger.info("Fetching articles for topic: %s", topic)

    try:
        # Guardian Articles
        guardian_articles = services.guardian.fetch_articles(
            query=topic,
            from_date=date
        )
        logger.info(
            "Stored %d Guardian articles for topic: %s",
            len(guardian_articles),
            topic
        )

        # News API Articles
        news_articles = services.news_api.fetch_articles(query=topic)
        logger.info(
            "Stored %d News API articles for topic: %s",
            len(news_articles),
            topic
        )

        # Reddit Posts
        reddit_posts = services.reddit.fetch_posts(topic=topic)
        if reddit_posts:
            logger.info(
                "Stored %d Reddit posts for topic: %s",
                len(reddit_posts),
                topic
            )

        time.sleep(1)  # Rate limiting

    except (ConnectionError, TimeoutError) as e:
        logger.error("Network error for topic '%s': %s", topic, str(e))
    except ValueError as e:
        logger.error("Invalid data for topic '%s': %s", topic, str(e))
    except KeyError as e:
        logger.error("Missing data for topic '%s': %s", topic, str(e))
    except (AttributeError, TypeError) as e:
        logger.error("Data processing error for topic '%s': %s", topic, str(e))

def generate_visualizations(services: NewsServices, topic: str, date: datetime) -> None:
    """Generate visualization for a given topic."""
    topic_data = services.analytics.get_topic_summary(topic, date)
    fig = services.visualization.create_topic_distribution_chart(topic_data)
    filename = f'topic_{topic.replace(" ", "_").lower()}.html'
    services.visualization.save_visualization(fig, filename)

def main():
    """Main execution function."""
    try:
        services = initialize_services()
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        yesterday_date = datetime.strptime(yesterday, '%Y-%m-%d')

        topics = [
            "technology",
            "artificial intelligence",
            "machine learning",
            "python programming"
        ]

        # Process articles
        for topic in topics:
            process_articles(services, topic, yesterday)

        # Generate analytics summary
        logger.info("Analytics Summary:")
        source_dist = services.analytics.get_source_distribution(yesterday_date)
        for source, count in source_dist:
            logger.info("%s: %d articles", source, count)

        # Setup reports directory in web/static
        reports_dir = os.path.join('web', 'static', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        services.visualization.reports_dir = reports_dir

        # Create source distribution visualization
        fig = services.visualization.create_source_distribution_chart(source_dist)
        services.visualization.save_visualization(fig, 'source_distribution.html')

        # Create topic visualizations
        for topic in topics:
            generate_visualizations(services, topic, yesterday_date)

    except Exception as e:
        logger.critical("Fatal error in main process: %s", str(e))
        raise SystemExit(1) from e

if __name__ == "__main__":
    try:
        # First run the main processing
        logger.info("Starting data processing...")
        main()

        # Then start the Flask app
        logger.info("Starting web interface...")
        app = create_app()
        app.run(host='0.0.0.0', port=5000, debug=True)

    except Exception as e:
        logger.critical("Application failed to start: %s", str(e))
        raise SystemExit(1) from e