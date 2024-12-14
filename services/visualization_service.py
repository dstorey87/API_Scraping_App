# services/visualization_service.py

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os
from database.articles_repository import ArticlesRepository
import logging

logger = logging.getLogger(__name__)

class VisualizationService:
    def __init__(self):
        self.db = ArticlesRepository()
        self.reports_dir = os.path.join('static', 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)

    def create_source_distribution_chart(self, data, top_n=20):
        """Create bar chart for top N sources"""
        df = pd.DataFrame(data, columns=['source', 'count'])
        df = df.nlargest(top_n, 'count')

        fig = go.Figure(data=[
            go.Bar(
                x=df['source'],
                y=df['count'],
                text=df['count'],
                textposition='auto',
            )
        ])

        fig.update_layout(
            title=f"Top {top_n} Sources by Article Count",
            xaxis_title="Source",
            yaxis_title="Number of Articles",
            xaxis_tickangle=-45
        )

        return fig

    def create_topic_distribution_chart(self, topic_data):
        """Create pie chart for topic distribution"""
        df = pd.DataFrame(topic_data, columns=['source', 'count'])
        fig = px.pie(df, values='count', names='source',
                    title=f"Article Distribution by Source for Topic")
        return fig

    def create_trend_chart(self, trend_data, topic):
        """Create line chart for topic trends"""
        df = pd.DataFrame(trend_data, columns=['date', 'count'])
        fig = px.line(df, x='date', y='count',
                      title=f"Trend Analysis for {topic}")
        return fig

    def save_visualization(self, fig, filename):
        """Save visualization to HTML file"""
        filepath = os.path.join(self.reports_dir, filename)
        fig.write_html(filepath)
        logger.info(f"Saved visualization to {filepath}")