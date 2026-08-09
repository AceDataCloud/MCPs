"""Unit tests for chat completion tools."""

import json

import pytest

from core.server import mcp
from tools import chat_tools


def test_openai_chat_completion_schema_includes_spec_params():
    """The MCP schema should expose optional fields from the OpenAPI request body."""
    tool = next(
        tool for tool in mcp._tool_manager.list_tools() if tool.name == "openai_chat_completion"
    )
    props = tool.parameters["properties"]

    for name in [
        "response_format",
        "tools",
        "tool_choice",
        "top_p",
        "frequency_penalty",
        "presence_penalty",
        "seed",
        "stop",
        "max_completion_tokens",
        "logprobs",
        "top_logprobs",
        "stream",
        "stream_options",
        "parallel_tool_calls",
        "user",
        "store",
        "metadata",
        "logit_bias",
        "modalities",
        "audio",
        "prediction",
        "web_search_options",
    ]:
        assert name in props


@pytest.mark.asyncio
async def test_openai_chat_completion_forwards_spec_params(monkeypatch):
    """Optional OpenAPI request fields must be forwarded unchanged."""
    captured: dict = {}

    async def mock_chat_completions(**kwargs):
        captured.update(kwargs)
        return {"choices": [{"message": {"content": "ok"}}]}

    monkeypatch.setattr(chat_tools.client, "chat_completions", mock_chat_completions)

    response_format = {"type": "json_object"}
    tools = [{"type": "function", "function": {"name": "lookup"}}]
    tool_choice = {"type": "function", "function": {"name": "lookup"}}
    await chat_tools.openai_chat_completion(
        messages=[{"role": "user", "content": "Hello"}],
        response_format=response_format,
        tools=tools,
        tool_choice=tool_choice,
        top_p=0.8,
        frequency_penalty=0.1,
        presence_penalty=0.2,
        seed=42,
        stop=["END"],
        max_completion_tokens=128,
        logprobs=True,
        top_logprobs=2,
        stream=True,
        stream_options={"include_usage": True},
        parallel_tool_calls=False,
        user="user-1",
        store=True,
        metadata={"trace": "abc"},
        logit_bias={"123": -1},
        modalities=["text"],
        audio={"voice": "alloy"},
        prediction={"type": "content", "content": "Hello"},
        web_search_options={"search_context_size": "low"},
    )

    assert captured["response_format"] is response_format
    assert captured["tools"] is tools
    assert captured["tool_choice"] is tool_choice
    assert captured["top_p"] == 0.8
    assert captured["frequency_penalty"] == 0.1
    assert captured["presence_penalty"] == 0.2
    assert captured["seed"] == 42
    assert captured["stop"] == ["END"]
    assert captured["max_completion_tokens"] == 128
    assert captured["logprobs"] is True
    assert captured["top_logprobs"] == 2
    assert captured["stream"] is True
    assert captured["stream_options"] == {"include_usage": True}
    assert captured["parallel_tool_calls"] is False
    assert captured["user"] == "user-1"
    assert captured["store"] is True
    assert captured["metadata"] == {"trace": "abc"}
    assert captured["logit_bias"] == {"123": -1}
    assert captured["modalities"] == ["text"]
    assert captured["audio"] == {"voice": "alloy"}
    assert captured["prediction"] == {"type": "content", "content": "Hello"}
    assert captured["web_search_options"] == {"search_context_size": "low"}


@pytest.mark.asyncio
async def test_openai_chat_completion_omits_none_spec_params(monkeypatch):
    """Optional fields should not be sent when omitted."""
    captured: dict = {}

    async def mock_chat_completions(**kwargs):
        captured.update(kwargs)
        return {"choices": [{"message": {"content": "ok"}}]}

    monkeypatch.setattr(chat_tools.client, "chat_completions", mock_chat_completions)

    response = await chat_tools.openai_chat_completion(
        messages=[{"role": "user", "content": "Hello"}]
    )

    assert json.loads(response)["choices"][0]["message"]["content"] == "ok"
    assert "response_format" not in captured
    assert "tools" not in captured
    assert "stream" not in captured
