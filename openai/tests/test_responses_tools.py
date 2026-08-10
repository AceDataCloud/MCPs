"""Unit tests for Responses API tools."""

import json

import pytest

from tools import responses_tools


@pytest.mark.asyncio
async def test_openai_create_response_forwards_spec_params(monkeypatch):
    captured_payload: dict[str, object] = {}

    async def mock_responses(**kwargs):
        captured_payload.update(kwargs)
        return {"id": "resp-1"}

    monkeypatch.setattr(responses_tools.client, "responses", mock_responses)

    response = await responses_tools.openai_create_response(
        input=[{"role": "user", "content": "hello"}],
        response_format={"type": "json_object"},
        stream=False,
        tools=[{"type": "web_search_preview"}],
    )

    assert captured_payload["response_format"] == {"type": "json_object"}
    assert captured_payload["stream"] is False
    assert captured_payload["tools"] == [{"type": "web_search_preview"}]
    assert json.loads(response) == {"id": "resp-1"}
