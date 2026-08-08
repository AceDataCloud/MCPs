"""Unit tests for Responses API tools."""

import pytest

from core.server import mcp
from tools import responses_tools


def test_openai_create_response_schema_includes_spec_params():
    """The MCP schema should expose optional fields from the OpenAPI request body."""
    tool = next(
        tool for tool in mcp._tool_manager.list_tools() if tool.name == "openai_create_response"
    )
    props = tool.parameters["properties"]

    assert "response_format" in props
    assert "tools" in props
    assert "stream" in props


@pytest.mark.asyncio
async def test_openai_create_response_forwards_spec_params(monkeypatch):
    """Responses API optional OpenAPI fields must be forwarded unchanged."""
    captured: dict = {}

    async def mock_responses(**kwargs):
        captured.update(kwargs)
        return {"output": [{"content": [{"text": "ok"}]}]}

    monkeypatch.setattr(responses_tools.client, "responses", mock_responses)

    response_format = {"type": "json_object"}
    tools = [{"type": "web_search_preview"}]
    await responses_tools.openai_create_response(
        input=[{"role": "user", "content": "Hello"}],
        response_format=response_format,
        tools=tools,
        stream=True,
    )

    assert captured["response_format"] is response_format
    assert captured["tools"] is tools
    assert captured["stream"] is True
