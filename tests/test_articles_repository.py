# tests/test_articles_repository.py

import pytest
from datetime import datetime
from unittest.mock import patch, Mock
from database.articles_repository import ArticlesRepository

@pytest.fixture
def mock_db_connection():
    """Create mock database connection."""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn

@pytest.fixture
def sample_article_data():
    """Create sample article data for testing."""
    return {
        'title': 'Test Article',
        'content': 'Test Content',
        'source': 'Test Source',
        'published_date': datetime.now()
    }

@pytest.fixture
def article_repository(mock_db_connection):
    """Create ArticlesRepository with mock connection."""
    with patch('database.articles_repository.get_db_connection') as mock_create:
        mock_create.return_value = mock_db_connection
        return ArticlesRepository()

def test_insert_article(article_repository, sample_article_data):
    """Test article insertion."""
    mock_cursor = article_repository.connection.cursor()
    mock_cursor.fetchone.return_value = (1,)

    article_id = article_repository.insert_article(
        title=sample_article_data['title'],
        content=sample_article_data['content'],
        source=sample_article_data['source'],
        published_date=sample_article_data['published_date']
    )

    assert article_id == 1
    mock_cursor.execute.assert_called_once()

def test_insert_guardian_article(article_repository):
    """Test Guardian article insertion."""
    mock_cursor = article_repository.connection.cursor()
    mock_cursor.fetchone.return_value = (1,)

    article_id = article_repository.insert_guardian_article(
        title="Test Guardian Article",
        url="https://www.theguardian.com/test",
        publication_date=datetime.now()
    )

    assert article_id == 1
    mock_cursor.execute.assert_called_once()

def test_insert_article_error(article_repository, sample_article_data):
    """Test error handling during article insertion."""
    mock_cursor = article_repository.connection.cursor()
    mock_cursor.execute.side_effect = Exception("Database error")

    with pytest.raises(Exception):
        article_repository.insert_article(
            title=sample_article_data['title'],
            content=sample_article_data['content'],
            source=sample_article_data['source'],
            published_date=sample_article_data['published_date']
        )

    article_repository.connection.rollback.assert_called_once()