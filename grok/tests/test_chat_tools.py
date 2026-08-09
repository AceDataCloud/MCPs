"""Unit tests for Grok chat tools."""

import json

import pytest

from tools import chat_tools


@pytest.mark.asyncio
async def test_grok_chat_completions_forwards_spec_params(monkeypatch):
    captured_payload: dict[str, object] = {}

    async def mock_chat_completions(**kwargs):
        captured_payload.update(kwargs)
        return {"id": "chat-1"}

    monkeypatch.setattr(chat_tools.client, "chat_completions", mock_chat_completions)

    response = await chat_tools.grok_chat_completions(
        messages=[{"role": "user", "content": "hello"}],
        n=2,
        max_completion_tokens=50,
        logprobs=True,
        top_logprobs=2,
        stream_options={"include_usage": True},
        parallel_tool_calls=False,
        store=False,
        metadata={"purpose": "test"},
        logit_bias={"42": -1},
        modalities=["text"],
        audio={"voice": "alloy", "format": "mp3"},
        prediction={"type": "content", "content": "hello"},
        web_search_options={"search_context_size": "low"},
    )

    assert captured_payload["n"] == 2
    assert captured_payload["max_completion_tokens"] == 50
    assert captured_payload["parallel_tool_calls"] is False
    assert captured_payload["web_search_options"] == {"search_context_size": "low"}
    assert json.loads(response) == {"id": "chat-1"}
