"""Unit tests for OpenAI informational tools."""

import json

import pytest

from tools import info_tools


@pytest.mark.asyncio
async def test_openai_get_models_calls_models_endpoint(monkeypatch):
    async def mock_models():
        return {"object": "list", "data": [{"id": "gpt-4.1"}]}

    monkeypatch.setattr(info_tools.client, "models", mock_models)

    response = await info_tools.openai_get_models()

    assert json.loads(response) == {"object": "list", "data": [{"id": "gpt-4.1"}]}


@pytest.mark.asyncio
async def test_openai_get_realtime_connection_info():
    response = await info_tools.openai_get_realtime_connection_info(model="gpt-realtime-2")
    payload = json.loads(response)

    assert payload["url"] == "wss://api.acedata.cloud/v1/realtime?model=gpt-realtime-2"
    assert payload["transport"] == "websocket"
