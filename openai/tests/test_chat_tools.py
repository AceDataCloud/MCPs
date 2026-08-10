"""Unit tests for chat completion tools."""

import json

import pytest

from tools import chat_tools


@pytest.mark.asyncio
async def test_openai_chat_completion_forwards_spec_params(monkeypatch, mock_chat_response):
    captured_payload: dict[str, object] = {}

    async def mock_chat_completions(**kwargs):
        captured_payload.update(kwargs)
        return mock_chat_response

    monkeypatch.setattr(chat_tools.client, "chat_completions", mock_chat_completions)

    response = await chat_tools.openai_chat_completion(
        messages=[{"role": "user", "content": "hello"}],
        stream=False,
        response_format={"type": "json_object"},
        tools=[{"type": "function", "function": {"name": "lookup"}}],
        tool_choice="auto",
        top_p=0.9,
        frequency_penalty=0.1,
        presence_penalty=0.2,
        seed=123,
        stop=["END"],
        max_completion_tokens=50,
        logprobs=True,
        top_logprobs=2,
        stream_options={"include_usage": True},
        parallel_tool_calls=False,
        user="user-1",
        store=False,
        metadata={"purpose": "test"},
        logit_bias={"42": -1},
        modalities=["text"],
        audio={"voice": "alloy", "format": "mp3"},
        prediction={"type": "content", "content": "hello"},
        web_search_options={"search_context_size": "low"},
    )

    assert captured_payload["stream"] is False
    assert captured_payload["response_format"] == {"type": "json_object"}
    assert captured_payload["tools"] == [{"type": "function", "function": {"name": "lookup"}}]
    assert captured_payload["tool_choice"] == "auto"
    assert captured_payload["max_completion_tokens"] == 50
    assert captured_payload["web_search_options"] == {"search_context_size": "low"}
    assert json.loads(response)["id"] == "chatcmpl-abc123"
