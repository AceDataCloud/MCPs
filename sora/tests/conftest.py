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
def mock_video_response():
    """Mock successful video generation response."""
    return {
        "success": True,
        "task_id": "test-task-123",
        "trace_id": "test-trace-456",
        "data": [
            {
                "id": "sora-2:task_01k7770rgsevxsmtpbn7xnm5gh",
                "video_url": "https://example.com/test-video.mp4",
                "state": "succeeded",
            }
        ],
    }


@pytest.fixture
def mock_task_response():
    """Mock task query response."""
    return {
        "id": "test-task-123",
        "created_at": 1705788000.0,
        "request": {
            "size": "large",
            "duration": 15,
            "orientation": "landscape",
            "prompt": "A cat running on the river",
            "model": "sora-2",
        },
        "response": {
            "success": True,
            "task_id": "test-task-123",
            "data": [
                {
                    "id": "sora-2:task_01k7770rgsevxsmtpbn7xnm5gh",
                    "video_url": "https://example.com/test-video.mp4",
                    "state": "succeeded",
                }
            ],
        },
    }


@pytest.fixture
def mock_batch_task_response():
    """Mock batch task query response."""
    return {
        "items": [
            {
                "id": "test-task-123",
                "created_at": 1705788000.0,
                "request": {
                    "size": "large",
                    "duration": 15,
                    "orientation": "landscape",
                    "prompt": "A cat running on the river",
                    "model": "sora-2",
                },
                "response": {
                    "success": True,
                    "task_id": "test-task-123",
                    "data": [
                        {
                            "id": "sora-2:task_01k7770rgsevxsmtpbn7xnm5gh",
                            "video_url": "https://example.com/test-video.mp4",
                            "state": "succeeded",
                        }
                    ],
                },
            }
        ],
        "count": 1,
    }


@pytest.fixture
def mock_async_response():
    """Mock async video generation response."""
    return {
        "task_id": "async-task-123",
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
