"""Shared Maestro MCP test fixtures."""

import pytest


@pytest.fixture
def api_token() -> str:
    return "test-token"
