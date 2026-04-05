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
                "id": "test-video-789",
                "model": "minimax-t2v",
                "prompt": "Test video prompt",
                "first_image_url": "",
                "video_url": "https://platform.cdn.acedata.cloud/hailuo/test-task-123.mp4",
                "status": "completed",
            }
        ],
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
            "model": "minimax-t2v",
        },
        "response": {
            "success": True,
            "task_id": "task-123",
            "trace_id": "trace-456",
            "data": [
                {
                    "id": "video-789",
                    "model": "minimax-t2v",
                    "prompt": "A test video",
                    "first_image_url": "",
                    "video_url": "https://platform.cdn.acedata.cloud/hailuo/task-123.mp4",
                    "status": "completed",
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
                "id": "task-123",
                "created_at": 1705788000.0,
                "request": {
                    "action": "generate",
                    "prompt": "First test video",
                    "model": "minimax-t2v",
                },
                "response": {
                    "success": True,
                    "task_id": "task-123",
                    "trace_id": "trace-456",
                    "data": [
                        {
                            "id": "video-789",
                            "model": "minimax-t2v",
                            "video_url": "https://platform.cdn.acedata.cloud/hailuo/task-123.mp4",
                            "status": "completed",
                        }
                    ],
                },
            },
            {
                "id": "task-456",
                "created_at": 1705788100.0,
                "request": {
                    "action": "generate",
                    "prompt": "Second test video",
                    "model": "minimax-i2v",
                },
                "response": {
                    "success": True,
                    "task_id": "task-456",
                    "trace_id": "trace-789",
                    "data": [
                        {
                            "id": "video-012",
                            "model": "minimax-i2v",
                            "video_url": "https://platform.cdn.acedata.cloud/hailuo/task-456.mp4",
                            "status": "completed",
                        }
                    ],
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
