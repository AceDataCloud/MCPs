"""Unit tests for embedding tools."""

import json

import pytest

from core.server import mcp
from tools import embedding_tools


def test_openai_embedding_schema_accepts_text_and_token_batches():
    """The MCP schema must expose every input shape accepted by the API."""
    tool = next(
        tool for tool in mcp._tool_manager.list_tools() if tool.name == "openai_create_embedding"
    )
    input_schema = tool.parameters["properties"]["input"]

    assert input_schema["anyOf"] == [
        {"minLength": 1, "type": "string"},
        {
            "items": {"minLength": 1, "type": "string"},
            "maxItems": 2048,
            "minItems": 1,
            "type": "array",
        },
        {
            "items": {"minimum": 0, "type": "integer"},
            "minItems": 1,
            "type": "array",
        },
        {
            "items": {
                "items": {"minimum": 0, "type": "integer"},
                "minItems": 1,
                "type": "array",
            },
            "maxItems": 2048,
            "minItems": 1,
            "type": "array",
        },
    ]
    assert "Never JSON-stringify an array" in input_schema["description"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "embedding_input",
    [
        ["first document", "second document"],
        [101, 102, 103],
        [[101, 102], [201, 202]],
    ],
)
async def test_openai_embedding_forwards_array_inputs(monkeypatch, embedding_input):
    """Text and token arrays must retain their shape in the API payload."""
    captured_payload: dict[str, object] = {}

    async def mock_embeddings(**kwargs):
        captured_payload.update(kwargs)
        return {"data": [{"embedding": [0.1]}, {"embedding": [0.2]}]}

    monkeypatch.setattr(embedding_tools.client, "embeddings", mock_embeddings)

    response = await embedding_tools.openai_create_embedding(input=embedding_input)

    assert captured_payload["input"] == embedding_input
    assert json.loads(response) == {"data": [{"embedding": [0.1]}, {"embedding": [0.2]}]}
