# tests/test_guardian_service.py

import pytest
from unittest.mock import patch
from datetime import datetime, timedelta
import requests
from services.guardian_service import GuardianService
from typing import Dict, Any

@pytest.fixture
def guardian_api_instance(monkeypatch) -> GuardianService:
    """Create a GuardianService instance with test configuration."""
    monkeypatch.setenv("GUARDIAN_API_KEY", "test_key")
    return GuardianService()

@pytest.fixture
def mock_api_response() -> Dict[str, Any]:
    """Return a mock API response."""
    return {
        "response": {
            "results": [{
                "webTitle": "Test Article",
                "webUrl": "https://test.com",
                "webPublicationDate": "2024-03-20T12:00:00Z"
            }]
        }
    }

def test_fetch_articles_integration() -> None:
    """Integration test for fetching articles."""
    service = GuardianService()
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    article_ids = service.fetch_articles(
        query="technology",
        from_date=yesterday
    )

    assert len(article_ids) > 0

def test_fetch_articles_unit(guardian_api_instance: GuardianService,
                           mock_api_response: Dict[str, Any]) -> None:
    """Unit test for fetching articles with mocked response."""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_api_response
        mock_get.return_value.raise_for_status.return_value = None

        results = guardian_api_instance.fetch_articles("test query")
        assert isinstance(results, list)
        assert len(results) == 1

def test_fetch_articles_api_error(guardian_api_instance: GuardianService) -> None:
    """Test error handling for API request failures."""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.RequestException

        with pytest.raises(requests.RequestException):
            guardian_api_instance.fetch_articles("test query")

def test_fetch_articles_invalid_response(guardian_api_instance: GuardianService) -> None:
    """Test error handling for invalid API responses."""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"invalid": "response"}
        mock_get.return_value.raise_for_status.return_value = None

        with pytest.raises(ValueError):
            guardian_api_instance.fetch_articles("test query")