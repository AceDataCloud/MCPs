"""Smoke tests for the Turnstile MCP server."""

import os
from unittest.mock import patch


def test_settings_defaults():
    from core.config import Settings

    with patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        assert settings.api_base_url == "https://api.acedata.cloud"
        assert settings.api_token == ""
        assert settings.server_name == "turnstile"
        assert settings.request_timeout == 120


def test_settings_token_from_env():
    from core.config import Settings

    with patch.dict(os.environ, {"ACEDATACLOUD_API_TOKEN": "test-token"}, clear=True):
        settings = Settings()
        assert settings.api_token == "test-token"
        assert settings.is_configured is True


def test_server_module_loads():
    from core.server import mcp

    assert mcp is not None


def test_tools_register():
    import tools  # noqa: F401
    from core.server import mcp

    expected = {
        "turnstile_get_token",
        "turnstile_get_task",
        "turnstile_get_usage_guide",
        "turnstile_get_api_info",
    }
    registered = {tool.name for tool in mcp._tool_manager.list_tools()}
    missing = expected - registered
    assert not missing, f"Missing tools: {missing}"


def test_prompts_register():
    import prompts  # noqa: F401
    from core.server import mcp

    expected = {"turnstile_guide", "turnstile_workflow_examples"}
    registered = {prompt.name for prompt in mcp._prompt_manager.list_prompts()}
    missing = expected - registered
    assert not missing, f"Missing prompts: {missing}"
