"""Pytest configuration and fixtures."""

import os
import sys
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Ensure a token is present BEFORE core.config is imported, so the global client
# and settings are constructed in a configured state for unit tests.
os.environ.setdefault("ACEDATACLOUD_PLATFORM_TOKEN", "test-token")
os.environ.setdefault("PLATFORM_API_BASE_URL", "https://platform.acedata.cloud")
os.environ.setdefault("LOG_LEVEL", "DEBUG")

BASE = "https://platform.acedata.cloud/api/v1"


@pytest.fixture
def base_url():
    return BASE


@pytest.fixture
def mock_services_page():
    return {
        "count": 2,
        "items": [
            {"id": "svc-1", "alias": "suno", "title": "Suno 音乐生成", "unit": "Credit"},
            {"id": "svc-2", "alias": "flux", "title": "Flux 图片生成", "unit": "Credit"},
        ],
    }


@pytest.fixture
def mock_applications_page():
    return {
        "count": 1,
        "items": [
            {
                "id": "app-1",
                "service_id": "svc-1",
                "remaining_amount": 100.5,
                "used_amount": 1.5,
                "scope": "Global",
            }
        ],
    }


@pytest.fixture
def mock_credential():
    return {
        "id": "cred-1",
        "name": "ci",
        "type": "Token",
        "token": "abcdef0123456789abcdef0123456789",
        "used_amount": 0.0,
    }
