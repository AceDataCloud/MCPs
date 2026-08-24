"""Smoke tests for webextrator MCP server."""

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


def test_extract_and_render_tools_match_openapi_request_fields():
    """Extract/render tools expose the documented async field, not legacy mode/cache fields."""
    import tools  # noqa: F401
    from core.server import mcp

    for tool_name in ("webextrator_extract", "webextrator_render"):
        schema = mcp._tool_manager._tools[tool_name].parameters
        properties = schema["properties"]

        assert "async" in properties
        assert "mode" not in properties
        assert "cookies" not in properties
        assert "bypass_cache" not in properties
        assert "cache_ttl_seconds" not in properties
