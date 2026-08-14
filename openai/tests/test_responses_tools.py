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
        tool_choice="auto",
        parallel_tool_calls=True,
        include=["output_text"],
        reasoning={"effort": "medium"},
        text={"format": {"type": "text"}},
        max_output_tokens=256,
        store=False,
        stream_options={"include_usage": True},
    )

    assert captured_payload["response_format"] == {"type": "json_object"}
    assert captured_payload["stream"] is False
    assert captured_payload["tools"] == [{"type": "web_search_preview"}]
    assert captured_payload["tool_choice"] == "auto"
    assert captured_payload["parallel_tool_calls"] is True
    assert captured_payload["include"] == ["output_text"]
    assert captured_payload["reasoning"] == {"effort": "medium"}
    assert captured_payload["text"] == {"format": {"type": "text"}}
    assert captured_payload["max_output_tokens"] == 256
    assert captured_payload["store"] is False
    assert captured_payload["stream_options"] == {"include_usage": True}
    assert json.loads(response) == {"id": "resp-1"}
