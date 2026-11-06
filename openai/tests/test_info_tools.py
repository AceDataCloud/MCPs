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
async def test_openai_list_chat_models_includes_sol_fast():
    text = await info_tools.openai_list_chat_models()
    assert "gpt-5.6-sol-fast" in text


@pytest.mark.asyncio
async def test_openai_list_image_models_names_all_gpt_image_2_5_variants():
    text = await info_tools.openai_list_image_models()
    assert "gpt-image-2.5-flare" in text
    assert "gpt-image-2.6-flare" in text
    assert "gpt-image-2.5-flare:reverse" in text
    assert "gpt-image-2.6-flare:reverse" in text
    assert "gpt-image-2.5-flare:official" in text
    assert "gpt-image-2.6-flare:official" in text
    assert "gpt-image-2.5-sunburst" in text
    assert "gpt-image-2.6-sunburst" in text
    assert "gpt-image-2.5-sunburst:reverse" in text
    assert "gpt-image-2.6-sunburst:reverse" in text
    assert "gpt-image-2.5-sunburst:official" in text
    assert "gpt-image-2.6-sunburst:official" in text
    assert "0.19 Credits/image" in text
    assert "per successful image" in text
    assert "requested model and per-image billing stay unchanged" in text
    assert "including :reverse and :official" in text
    assert "gpt-image-2.5 |" not in text
    assert "gpt-image-2.5:reverse" not in text


@pytest.mark.asyncio
async def test_image_model_guide_covers_gpt_image_2_6_contract():
    text = await info_tools.openai_list_image_models()

    assert "GPT Image 2/2.5/2.6 custom dimensions" in text
    assert "GPT Image 2.5/2.6 Flare/Sunburst only" in text
    assert (
        "GPT Image 2.6 unsuffixed models and their :reverse aliases bill per successful image"
        in text
    )
    assert "0.22 Credits/image" in text
    assert "2.0/2.5 reverse requests may be fulfilled" in text
    assert "GPT Image 2.6 has no cross-model fallback" in text
    assert "same token rates as 2.5" in text
    assert "not fixed per-image charges" in text
    assert "Static PNG/JPEG/WebP" in text
    assert "Native GIF generation/editing" in text
    assert "Ordinary/reverse Sunburst GIF is not available" in text
    assert "not gpt-image-2.6 or a bare :reverse/:official alias" in text
