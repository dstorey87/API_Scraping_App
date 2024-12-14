import pytest
from datetime import datetime
from unittest.mock import Mock

@pytest.fixture
def mock_db_connection():
    """Create mock database connection."""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn

@pytest.fixture
def sample_article_data():
    """Sample article data for tests."""
    return {
        'title': 'Test Article',
        'content': 'Test Content',
        'source': 'Test Source',
        'published_date': datetime.now()
    }