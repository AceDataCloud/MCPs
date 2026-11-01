"""Regressions for documented chat streaming and model discovery contracts."""

import json
from typing import get_args
from unittest.mock import AsyncMock

import pytest

import tools  # noqa: F401
from core.server import mcp
from tools import chat_tools, info_tools


@pytest.mark.asyncio
@pytest.mark.parametrize("model", ["mimo-v2.6-pro", "mimo-v2.6-flash"])
async def test_mimo_text_chat_reaches_http(monkeypatch, model):
    import httpx

    captured = {}

    async def post(_client, url, **kwargs):
        captured.update(kwargs["json"])
        assert url == "https://api.acedata.cloud/openai/chat/completions"
        return httpx.Response(200, json={}, request=httpx.Request("POST", url))

    monkeypatch.setattr(httpx.AsyncClient, "post", post)
    monkeypatch.setattr(chat_tools.client, "api_token", "test-token")
    messages = [
        {
            "role": "assistant",
            "content": None,
            "reasoning_content": "reasoning",
            "tool_calls": [
                {
                    "id": "call-1",
                    "type": "function",
                    "function": {"name": "lookup", "arguments": "{}"},
                }
            ],
        },
        {"role": "tool", "tool_call_id": "call-1", "content": "result"},
    ]
    await mcp.call_tool(
        "openai_chat_completion",
        {
            "model": model,
            "messages": messages,
            "thinking": {"type": "disabled"},
            "max_completion_tokens": 256,
            "tool_choice": "auto",
            "stream": False,
        },
    )
    assert captured == {
        "model": model,
        "messages": messages,
        "thinking": {"type": "disabled"},
        "max_completion_tokens": 256,
        "tool_choice": "auto",
        "stream": False,
    }
    schema = mcp._tool_manager._tools["openai_create_response"].parameters
    assert model not in schema["properties"]["model"]["enum"]


@pytest.mark.asyncio
@pytest.mark.parametrize("effort", ["low", "medium", "high", "xhigh", "max"])
async def test_terra_reasoning_levels(monkeypatch, effort):
    request = AsyncMock(return_value={"id": "test-response"})
    monkeypatch.setattr(chat_tools.client, "chat_completions", request)
    await mcp.call_tool(
        "openai_chat_completion",
        {
            "model": "gpt-6.1-terra",
            "messages": [{"role": "user", "content": "hello"}],
            "reasoning_effort": effort,
        },
    )
    assert request.await_args.kwargs["reasoning_effort"] == effort


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
