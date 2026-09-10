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
async def test_openai_get_realtime_connection_info_calls_realtime_endpoint(monkeypatch):
    async def mock_realtime(model, voice):
        return {
            "url": f"wss://api.test.com/v1/realtime?model={model}&voice={voice}",
            "model": model,
            "voice": voice,
        }

    monkeypatch.setattr(info_tools.client, "realtime", mock_realtime)

    response = await info_tools.openai_get_realtime_connection_info(
        model="gpt-realtime-2.1-mini",
        voice="marin",
    )
    payload = json.loads(response)

    assert (
        payload["url"] == "wss://api.test.com/v1/realtime?model=gpt-realtime-2.1-mini&voice=marin"
    )
    assert payload["voice"] == "marin"


@pytest.mark.asyncio
async def test_openai_list_image_models_names_all_gpt_image_2_5_variants():
    text = await info_tools.openai_list_image_models()
    assert "gpt-image-2.5-flare" in text
    assert "gpt-image-2.5-flare:official" in text
    assert "gpt-image-2.5-sunburst" in text
    assert "gpt-image-2.5-sunburst:official" in text
    assert "gpt-image-2.5 |" not in text
