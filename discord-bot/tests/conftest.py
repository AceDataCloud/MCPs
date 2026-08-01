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
def bot_token():
    """Get bot token from environment for integration tests."""
    token = os.environ.get("DISCORD_BOT_TOKEN", "")
    if not token:
        pytest.skip("DISCORD_BOT_TOKEN not configured for integration tests")
    return token


@pytest.fixture
def bot_base_url():
    """Get bot base URL from environment for integration tests."""
    url = os.environ.get("DISCORD_BOT_BASE_URL", "")
    if not url:
        pytest.skip("DISCORD_BOT_BASE_URL not configured for integration tests")
    return url


@pytest.fixture
def mock_whoami_response():
    """Mock successful whoami response."""
    return {
        "id": "123456789012345678",
        "username": "TestBot",
        "discriminator": "0",
        "avatar": "abcdef1234567890",
    }


@pytest.fixture
def mock_guilds_response():
    """Mock successful guilds response."""
    return [
        {"id": "111111111111111111", "name": "Test Server 1"},
        {"id": "222222222222222222", "name": "Test Server 2"},
    ]


@pytest.fixture
def mock_channels_response():
    """Mock successful channels response."""
    return [
        {"id": "333333333333333333", "name": "general", "type": 0},
        {"id": "444444444444444444", "name": "announcements", "type": 0},
    ]


@pytest.fixture
def mock_messages_response():
    """Mock successful messages response."""
    return [
        {
            "id": "555555555555555555",
            "content": "Hello, world!",
            "author": {"id": "123456789012345678", "username": "TestBot"},
            "timestamp": "2026-08-01T00:00:00.000Z",
        },
        {
            "id": "666666666666666666",
            "content": "How are you?",
            "author": {"id": "987654321098765432", "username": "AnotherUser"},
            "timestamp": "2026-08-01T00:01:00.000Z",
        },
    ]


@pytest.fixture
def mock_message_response():
    """Mock successful single message response."""
    return {
        "id": "555555555555555555",
        "content": "Hello, world!",
        "author": {"id": "123456789012345678", "username": "TestBot"},
        "timestamp": "2026-08-01T00:00:00.000Z",
        "channel_id": "333333333333333333",
    }


@pytest.fixture
def mock_error_response():
    """Mock error response."""
    return {"error": "Invalid channel ID"}
