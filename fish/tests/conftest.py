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
def mock_audio_response():
    """Mock successful audio generation response."""
    return {
        "success": True,
        "task_id": "test-task-123",
        "trace_id": "test-trace-456",
        "data": [
            {
                "prompt": "Hello, how are you today?",
                "audio_url": "https://platform.cdn.acedata.cloud/fish/test-task-123.mp3",
            }
        ],
    }


@pytest.fixture
def mock_voice_response():
    """Mock successful voice creation response."""
    return {
        "success": True,
        "task_id": "test-voice-task-123",
        "trace_id": "test-trace-456",
        "data": [
            {
                "voice_id": "abc123def456",
                "title": "My Custom Voice",
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
            "action": "speech",
            "prompt": "Hello world",
            "voice_id": "d7900c21663f485ab63ebdb7e5905036",
            "model": "fish-tts",
        },
        "response": {
            "success": True,
            "task_id": "task-123",
            "trace_id": "trace-456",
            "data": [
                {
                    "prompt": "Hello world",
                    "audio_url": "https://platform.cdn.acedata.cloud/fish/task-123.mp3",
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
                    "action": "speech",
                    "prompt": "First test audio",
                    "model": "fish-tts",
                },
                "response": {
                    "success": True,
                    "task_id": "task-123",
                    "trace_id": "trace-456",
                    "data": [
                        {
                            "prompt": "First test audio",
                            "audio_url": "https://platform.cdn.acedata.cloud/fish/task-123.mp3",
                        }
                    ],
                },
            },
            {
                "id": "task-456",
                "created_at": 1705788100.0,
                "request": {
                    "action": "speech",
                    "prompt": "Second test audio",
                    "model": "fish-tts",
                },
                "response": {
                    "success": True,
                    "task_id": "task-456",
                    "trace_id": "trace-789",
                    "data": [
                        {
                            "prompt": "Second test audio",
                            "audio_url": "https://platform.cdn.acedata.cloud/fish/task-456.mp3",
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
