"""Smoke tests for the Localization MCP server."""

import json
import os
from unittest.mock import AsyncMock, patch

import pytest


def test_settings_defaults():
    from core.config import Settings

    with patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        assert settings.api_base_url == "https://api.acedata.cloud"
        assert settings.api_token == ""
        assert settings.server_name == "localization"
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
        "localization_translate",
        "localization_get_usage_guide",
        "localization_get_api_info",
    }
    registered = {tool.name for tool in mcp._tool_manager.list_tools()}
    missing = expected - registered
    assert not missing, f"Missing tools: {missing}"

    schema = mcp._tool_manager._tools["localization_translate"].parameters
    assert set(schema["required"]) == {"input", "locale", "extension"}
    assert schema["properties"]["locale"]["enum"] == [
        "en",
        "de",
        "pt",
        "es",
        "fr",
        "zh-CN",
        "zh-TW",
        "it",
        "ko",
        "ja",
        "ru",
        "pl",
        "fi",
        "sv",
        "el",
        "uk",
        "ar",
        "sr",
    ]
    assert schema["properties"]["extension"]["enum"] == ["md", "json"]
    assert schema["properties"]["model"]["anyOf"][0]["enum"] == ["gpt-3.5", "gpt-4"]


@pytest.mark.asyncio
async def test_fastmcp_dispatch_calls_translate_tool():
    import tools  # noqa: F401
    from core.server import mcp
    from tools import localization_tools

    with patch.object(
        localization_tools.client, "translate", new_callable=AsyncMock
    ) as translate:
        translate.return_value = {"data": {"hello": "Hallo"}, "locale": "de"}

        result = await mcp.call_tool(
            "localization_translate",
            {"input": {"hello": "Hello"}, "locale": "de", "extension": "json"},
        )

    assert result
    translate.assert_awaited_once_with(
        input={"hello": "Hello"},
        locale="de",
        extension="json",
        model=None,
    )


@pytest.mark.asyncio
async def test_translate_tool_sends_openapi_payload():
    from tools.localization_tools import localization_translate

    with patch("tools.localization_tools.client.translate", new_callable=AsyncMock) as translate:
        translate.return_value = {"data": {"hello": "Hallo"}, "locale": "de", "model": "gpt-4"}

        result = await localization_translate(
            input={"hello": "Hello"},
            locale="de",
            extension="json",
            model="gpt-4",
        )

    translate.assert_awaited_once_with(
        input={"hello": "Hello"},
        locale="de",
        extension="json",
        model="gpt-4",
    )
    assert json.loads(result) == {"data": {"hello": "Hallo"}, "locale": "de", "model": "gpt-4"}


def test_prompts_register():
    import prompts  # noqa: F401
    from core.server import mcp

    expected = {"localization_guide", "localization_workflow_examples"}
    registered = {prompt.name for prompt in mcp._prompt_manager.list_prompts()}
    missing = expected - registered
    assert not missing, f"Missing prompts: {missing}"
