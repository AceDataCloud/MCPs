"""Pytest configuration and fixtures."""

import os
import sys
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load .env file BEFORE any other imports
from dotenv import load_dotenv

load_dotenv(dotenv_path=project_root / ".env")

# Set default log level for tests
os.environ.setdefault("LOG_LEVEL", "DEBUG")


@pytest.fixture
def api_token():
    """Get API token from environment for integration tests."""
    token = os.environ.get("ACEDATACLOUD_API_TOKEN", "")
    if not token:
        pytest.skip("ACEDATACLOUD_API_TOKEN not configured for integration tests")
    return token


@pytest.fixture
def mock_search_response():
    """Mock successful search response."""
    return {
        "knowledge_graph": {
            "title": "Apple",
            "type": "Technology company",
            "website": "http://www.apple.com/",
            "description": "Apple Inc. is an American multinational corporation...",
            "attributes": {
                "CEO": "Tim Cook",
                "Founded": "April 1, 1976",
                "Headquarters": "Cupertino, CA",
            },
        },
        "organic": [
            {
                "title": "Apple",
                "link": "https://www.apple.com/",
                "snippet": "Discover the innovative world of Apple...",
                "position": 1,
            },
            {
                "title": "Apple Inc. - Wikipedia",
                "link": "https://en.wikipedia.org/wiki/Apple_Inc.",
                "snippet": "Apple Inc. is an American multinational corporation...",
                "position": 2,
            },
        ],
        "people_also_ask": [
            {
                "question": "What is Apple Inc?",
                "snippet": "Apple Inc. is a multinational technology company...",
                "link": "https://en.wikipedia.org/wiki/Apple_Inc.",
            },
        ],
        "related_searches": [
            {"query": "Apple iPhone"},
            {"query": "Apple stock"},
        ],
    }


@pytest.fixture
def mock_images_response():
    """Mock successful images search response."""
    return {
        "images": [
            {
                "title": "Apple Logo",
                "link": "https://example.com/apple-logo",
                "image_url": "https://example.com/apple-logo.jpg",
            },
            {
                "title": "iPhone 15",
                "link": "https://example.com/iphone",
                "image_url": "https://example.com/iphone.jpg",
            },
        ],
    }


@pytest.fixture
def mock_news_response():
    """Mock successful news search response."""
    return {
        "news": [
            {
                "title": "Apple Announces New Product",
                "link": "https://news.example.com/apple",
                "snippet": "Apple Inc. today announced...",
                "source": "Tech News",
                "date": "2 hours ago",
            },
        ],
    }


@pytest.fixture
def mock_error_response():
    """Mock error response."""
    return {
        "success": False,
        "error": {
            "code": "invalid_request",
            "message": "Invalid parameters provided",
        },
    }
