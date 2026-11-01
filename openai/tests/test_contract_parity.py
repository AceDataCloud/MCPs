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
            "openai_chat_completion",
            "chat_completions",
            {"messages": [{"role": "user", "content": "hello"}]},
        ),
        ("openai_create_response", "responses", {"input": "hello"}),
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
            "openai_chat_completion",
            "chat_completions",
            {"messages": [{"role": "user", "content": "hello"}]},
        ),
        ("openai_create_response", "responses", {"input": "hello"}),
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
async def test_model_discovery_matches_each_tool_enum():
    from core.types import ChatModel, ResponsesModel

    listing = await info_tools.openai_list_chat_models()
    chat, responses = listing.split("## openai_create_response", 1)

    def listed(text):
        return {line[2:] for line in text.splitlines() if line.startswith("- ")}

    assert listed(chat) == set(get_args(ChatModel))
    assert listed(responses) == set(get_args(ResponsesModel))


@pytest.mark.asyncio
async def test_task_count_mode_is_exposed_and_forwarded(monkeypatch):
    from tools import tasks_tools

    request = AsyncMock(return_value={"items": [], "count": 0, "count_exact": True})
    monkeypatch.setattr(tasks_tools.client, "tasks", request)
    await mcp.call_tool("openai_list_tasks", {"ids": ["task-1"], "count_mode": "exact"})
    assert request.await_args.kwargs == {
        "action": "retrieve_batch",
        "ids": ["task-1"],
        "count_mode": "exact",
    }
    await mcp.call_tool("openai_list_tasks", {"ids": ["task-1"]})
    assert request.await_args.kwargs["count_mode"] == "none"
