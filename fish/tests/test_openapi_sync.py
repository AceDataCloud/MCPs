"""Tests for Fish OpenAPI sync behavior."""

import json

from tools import audio_tools, info_tools


async def test_fish_generate_audio_maps_openapi_fields(monkeypatch) -> None:
    captured: dict = {}

    async def fake_generate_audio(**kwargs):
        captured.update(kwargs)
        return {"audio_url": "https://example.com/audio.mp3"}

    monkeypatch.setattr(audio_tools.client, "generate_audio", fake_generate_audio)

    response = await audio_tools.fish_generate_audio(
        text="Hello from Fish",
        reference_id="voice-123",
        model="s1",
        format="mp3",
        sample_rate=16000,
        latency="balanced",
    )

    data = json.loads(response)
    assert data["audio_url"] == "https://example.com/audio.mp3"
    assert captured["text"] == "Hello from Fish"
    assert captured["reference_id"] == "voice-123"
    assert captured["model"] == "s1"
    assert captured["format"] == "mp3"
    assert captured["sample_rate"] == 16000
    assert captured["latency"] == "balanced"


async def test_fish_generate_audio_supports_legacy_aliases(monkeypatch) -> None:
    captured: dict = {}

    async def fake_generate_audio(**kwargs):
        captured.update(kwargs)
        return {"audio_url": "https://example.com/audio.mp3"}

    monkeypatch.setattr(audio_tools.client, "generate_audio", fake_generate_audio)

    response = await audio_tools.fish_generate_audio(
        prompt="Legacy prompt field",
        voice_id="legacy-voice-id",
    )

    data = json.loads(response)
    assert data["audio_url"] == "https://example.com/audio.mp3"
    assert captured["text"] == "Legacy prompt field"
    assert captured["reference_id"] == "legacy-voice-id"
    assert captured["model"] == "s2-pro"


async def test_fish_list_models_maps_openapi_query_params(monkeypatch) -> None:
    captured: dict = {}

    async def fake_list_models(**kwargs):
        captured.update(kwargs)
        return {"total": 1, "items": [{"_id": "voice-1"}]}

    monkeypatch.setattr(info_tools.client, "list_models", fake_list_models)

    response = await info_tools.fish_list_models(
        page_size=10,
        page_number=2,
        title="Marcus",
        self_only=True,
    )

    data = json.loads(response)
    assert data["total"] == 1
    assert captured == {
        "page_size": 10,
        "page_number": 2,
        "title": "Marcus",
        "self": True,
    }


async def test_fish_get_model_calls_model_detail_endpoint(monkeypatch) -> None:
    async def fake_get_model(model_id: str):
        return {"_id": model_id, "title": "Sample voice"}

    monkeypatch.setattr(info_tools.client, "get_model", fake_get_model)

    response = await info_tools.fish_get_model("voice-xyz")
    data = json.loads(response)

    assert data["_id"] == "voice-xyz"
