"""Regressions for documented chat streaming and model discovery contracts."""

import json
from unittest.mock import AsyncMock

import pytest

import tools  # noqa: F401
from core.server import mcp
from tools import chat_tools


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool_name", "client_method", "arguments"),
    [
        (
            "glm_chat_completions",
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
            "glm_chat_completions",
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
