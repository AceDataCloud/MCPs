"""Smoke tests for glm MCP server."""

import os
from unittest.mock import patch


def test_settings_defaults():
    """Settings load with sensible defaults."""
    from core.config import Settings

    with patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        assert settings.api_base_url == "https://api.acedata.cloud"
        assert settings.api_token == ""


def test_settings_token_from_env():
    """Settings pick up ACEDATACLOUD_API_TOKEN."""
    from core.config import Settings

    with patch.dict(os.environ, {"ACEDATACLOUD_API_TOKEN": "test-token"}, clear=True):
        settings = Settings()
        assert settings.api_token == "test-token"


def test_server_module_loads():
    """The MCP server module loads without errors."""
    from core.server import mcp

    assert mcp is not None
