"""Regressions for documented chat streaming and model discovery contracts."""

import json
from typing import get_args
from unittest.mock import AsyncMock

import pytest

import tools  # noqa: F401
from core.server import mcp
from tools import chat_tools, info_tools


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool_name", "client_method", "arguments"),
    [
        (
            "grok_chat_completions",
            "chat_completions",
            {"messages": [{"role": "user", "content": "hello"}]},
        )
    ],
)
async def test_stream_true_fails_before_api_request(
    monkeypatch, tool_name, client_method, arguments
):
    request = AsyncMock()
    monkeypatch.setattr(chat_tools.client, client_method, request)
    content, _ = await mcp.call_tool(tool_name, {**arguments, "stream": True})
    result = json.loads(content[0].text)
    assert result["code"] == "streaming_not_supported"
    assert "No API request was sent" in result["message"]
    request.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool_name", "client_method", "arguments"),
    [
        (
            "grok_chat_completions",
            "chat_completions",
            {"messages": [{"role": "user", "content": "hello"}]},
        )
    ],
)
async def test_non_streaming_keeps_complete_result(
    monkeypatch, tool_name, client_method, arguments
):
    response = {"id": "response-1", "choices": [{"message": {"content": "hello"}}]}
    request = AsyncMock(return_value=response)
    monkeypatch.setattr(chat_tools.client, client_method, request)
    content, _ = await mcp.call_tool(tool_name, {**arguments, "stream": False})
    assert json.loads(content[0].text) == response
    assert request.await_args.kwargs["stream"] is False


@pytest.mark.asyncio
async def test_model_discovery_and_default_match_tool_schema():
    from core.types import DEFAULT_CHAT_MODEL, GrokChatModel, GrokVideoModel

    listing = await info_tools.grok_list_models()
    chat, rest = listing.split("Available Grok Imagine Video Models", 1)
    video = rest.split("Usage:", 1)[0]
    assert {line[2:] for line in chat.splitlines() if line.startswith("- ")} == set(
        get_args(GrokChatModel)
    )
    assert {line[2:] for line in video.splitlines() if line.startswith("- ")} == set(
        get_args(GrokVideoModel)
    )
    assert f"default {DEFAULT_CHAT_MODEL}" in chat
    schema = mcp._tool_manager._tools["grok_chat_completions"].parameters["properties"]["model"]
    assert schema["default"] == DEFAULT_CHAT_MODEL
    assert f"{DEFAULT_CHAT_MODEL} (default)" in schema["description"]
