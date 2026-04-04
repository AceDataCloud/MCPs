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
        "video_id": "test-video-456",
        "prompt": "Test video prompt",
        "video_url": "https://platform.cdn.acedata.cloud/luma/test-task-123.mp4",
        "video_width": 1360,
        "video_height": 752,
        "state": "completed",
        "thumbnail_url": "https://platform.cdn.acedata.cloud/luma/test-task-123.jpg",
        "thumbnail_width": 1360,
        "thumbnail_height": 752,
    }


@pytest.fixture
def mock_task_response():
    """Mock task query response."""
    return {
        "id": "task-123",
        "created_at": 1705788000.0,
        "request": {
            "action": "generate",
            "prompt": "A test video",
        },
        "response": {
            "success": True,
            "task_id": "task-123",
            "video_id": "video-456",
            "prompt": "A test video",
            "video_url": "https://platform.cdn.acedata.cloud/luma/task-123.mp4",
            "video_width": 1360,
            "video_height": 752,
            "state": "completed",
            "thumbnail_url": "https://platform.cdn.acedata.cloud/luma/task-123.jpg",
            "thumbnail_width": 1360,
            "thumbnail_height": 752,
        },
    }


@pytest.fixture
def mock_batch_task_response():
    """Mock batch task query response."""
    return {
        "items": [
            {
                "id": "task-123",
                "created_at": 1705788000.0,
                "request": {
                    "action": "generate",
                    "prompt": "First test video",
                },
                "response": {
                    "success": True,
                    "task_id": "task-123",
                    "video_id": "video-456",
                    "video_url": "https://platform.cdn.acedata.cloud/luma/task-123.mp4",
                    "state": "completed",
                },
            },
            {
                "id": "task-789",
                "created_at": 1705788100.0,
                "request": {
                    "action": "generate",
                    "prompt": "Second test video",
                },
                "response": {
                    "success": True,
                    "task_id": "task-789",
                    "video_id": "video-012",
                    "video_url": "https://platform.cdn.acedata.cloud/luma/task-789.mp4",
                    "state": "completed",
                },
            },
        ],
        "count": 2,
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
