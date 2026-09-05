"""Guards the Fish TTS MCP surface against the API contract."""

from typing import get_args

import httpx
import pytest

from core.client import FishClient
from core.exceptions import FishAPIError
from core.server import mcp
from core.types import DEFAULT_MODEL, FishModel, FishMp3Bitrate, FishReferenceId
from tools import audio_tools, info_tools  # noqa: F401

# Mirrors the `model` header-param enum in the Fish TTS OpenAPI spec.
SPEC_MODELS = {"s1", "s2-pro", "s2.1-pro"}


def test_models_match_spec():
    assert set(get_args(FishModel)) == SPEC_MODELS


def test_default_model_is_selectable():
    assert DEFAULT_MODEL in get_args(FishModel)


def test_mp3_bitrate_matches_spec():
    assert set(get_args(FishMp3Bitrate)) == {64, 128, 192}


def test_reference_id_matches_spec():
    assert get_args(FishReferenceId) == (str, list[str])


def test_generate_audio_exposes_async_request_control():
    schema = mcp._tool_manager._tools["fish_generate_audio"].parameters
    properties = schema["properties"]

    assert "async" in properties
    assert {"type": "boolean"} in properties["async"]["anyOf"]


def test_generate_audio_exposes_reference_id_array():
    schema = mcp._tool_manager._tools["fish_generate_audio"].parameters
    reference_id_schema = schema["properties"]["reference_id"]

    assert {"type": "string"} in reference_id_schema["anyOf"]
    assert {"type": "array", "items": {"type": "string"}} in reference_id_schema["anyOf"]


@pytest.mark.asyncio
async def test_generate_audio_forwards_reference_id_array(monkeypatch):
    captured = {}

    async def mock_generate_audio(**kwargs):
        captured.update(kwargs)
        return {"task_id": "task-1"}

    monkeypatch.setattr(audio_tools.client, "generate_audio", mock_generate_audio)

    await audio_tools.fish_generate_audio(text="hello", reference_id=["voice-1", "voice-2"])

    assert captured["reference_id"] == ["voice-1", "voice-2"]


def test_list_models_uses_spec_self_parameter():
    schema = mcp._tool_manager._tools["fish_list_models"].parameters
    properties = schema["properties"]

    assert "self" in properties
    assert "self_only" not in properties


def test_async_callback_preserves_explicit_false():
    client = FishClient(api_token="test-token", base_url="https://api.test.com")

    assert client._with_async_callback({"async": False})["async"] is False


def test_forbidden_is_api_error():
    client = FishClient(api_token="test-token", base_url="https://api.test.com")
    response = httpx.Response(
        403,
        json={"error": {"code": "used_up", "message": "funds"}},
        request=httpx.Request("POST", "https://api.test.com/fish/tts"),
    )

    with pytest.raises(FishAPIError, match="funds") as exc_info:
        client._handle_error_response(response)

    assert exc_info.value.status_code == 403
    assert exc_info.value.code == "used_up"
