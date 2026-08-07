"""Smoke tests for the HCaptcha MCP server."""

import os
from unittest.mock import patch

import pytest


def test_settings_defaults():
    from core.config import Settings

    with patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        assert settings.api_base_url == "https://api.acedata.cloud"
        assert settings.api_token == ""
        assert settings.server_name == "hcaptcha"
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

    expected = {"hcaptcha_recognize", "hcaptcha_get_token", "hcaptcha_get_task", "hcaptcha_get_usage_guide", "hcaptcha_get_api_info"}
    registered = {tool.name for tool in mcp._tool_manager.list_tools()}
    missing = expected - registered
    assert not missing, f"Missing tools: {missing}"


def test_prompts_register():
    import prompts  # noqa: F401
    from core.server import mcp

    expected = {"hcaptcha_guide", "hcaptcha_workflow_examples"}
    registered = {prompt.name for prompt in mcp._prompt_manager.list_prompts()}
    missing = expected - registered
    assert not missing, f"Missing prompts: {missing}"


@pytest.mark.asyncio
async def test_get_token_includes_optional_rqdata():
    from core.client import HCaptchaClient

    captured = {}
    client = HCaptchaClient(api_token="test-token")

    async def fake_request(method, endpoint, *, payload=None, timeout=None):
        captured.update({"method": method, "endpoint": endpoint, "payload": payload, "timeout": timeout})
        return {"success": True}

    client.request = fake_request

    result = await client.get_token(
        website_key="site-key",
        website_url="https://example.com",
        rqdata="rqdata-value",
        proxy="http://proxy.example:8080",
        mode="sync",
    )

    assert result == {"success": True}
    assert captured["method"] == "POST"
    assert captured["endpoint"] == "/captcha/token/hcaptcha"
    assert captured["payload"] == {
        "website_key": "site-key",
        "website_url": "https://example.com",
        "rqdata": "rqdata-value",
        "proxy": "http://proxy.example:8080",
    }
