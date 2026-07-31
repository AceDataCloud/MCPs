"""Unit tests for audio speech tools."""

import base64
import json

import pytest

from core.server import mcp
from tools import audio_tools


def test_openai_text_to_speech_registered():
    """The openai_text_to_speech tool must be registered with the MCP server."""
    tool_names = [tool.name for tool in mcp._tool_manager.list_tools()]
    assert "openai_text_to_speech" in tool_names


def test_openai_text_to_speech_schema():
    """The MCP schema for openai_text_to_speech must include all expected parameters."""
    tool = next(
        tool for tool in mcp._tool_manager.list_tools() if tool.name == "openai_text_to_speech"
    )
    props = tool.parameters["properties"]
    assert "input" in props
    assert "model" in props
    assert "voice" in props
    assert "response_format" in props
    assert "speed" in props
    assert "input" in tool.parameters.get("required", [])


@pytest.mark.asyncio
async def test_openai_text_to_speech_returns_base64_audio(monkeypatch):
    """Tool must return base64-encoded audio bytes with format metadata."""
    fake_audio = b"fake-mp3-audio-data"

    async def mock_audio_speech(**_kwargs):
        return fake_audio

    monkeypatch.setattr(audio_tools.client, "audio_speech", mock_audio_speech)

    response = await audio_tools.openai_text_to_speech(input="Hello world")

    result = json.loads(response)
    assert result["encoding"] == "base64"
    assert result["format"] == "mp3"
    assert result["size_bytes"] == len(fake_audio)
    assert base64.b64decode(result["audio"]) == fake_audio


@pytest.mark.asyncio
async def test_openai_text_to_speech_forwards_all_params(monkeypatch):
    """All parameters must be forwarded correctly to the client."""
    captured: dict = {}

    async def mock_audio_speech(**kwargs):
        captured.update(kwargs)
        return b"audio"

    monkeypatch.setattr(audio_tools.client, "audio_speech", mock_audio_speech)

    await audio_tools.openai_text_to_speech(
        input="Test text",
        model="tts-1",
        voice="nova",
        response_format="opus",
        speed=1.5,
    )

    assert captured["model"] == "tts-1"
    assert captured["input"] == "Test text"
    assert captured["voice"] == "nova"
    assert captured["response_format"] == "opus"
    assert captured["speed"] == 1.5


@pytest.mark.asyncio
async def test_openai_text_to_speech_omits_none_speed(monkeypatch):
    """Speed must not be included in the payload when not provided."""
    captured: dict = {}

    async def mock_audio_speech(**kwargs):
        captured.update(kwargs)
        return b"audio"

    monkeypatch.setattr(audio_tools.client, "audio_speech", mock_audio_speech)

    await audio_tools.openai_text_to_speech(input="Hello")

    assert "speed" not in captured


@pytest.mark.asyncio
async def test_openai_text_to_speech_handles_empty_response(monkeypatch):
    """Empty response from the API must return an error JSON."""

    async def mock_audio_speech(**_kwargs):
        return b""

    monkeypatch.setattr(audio_tools.client, "audio_speech", mock_audio_speech)

    response = await audio_tools.openai_text_to_speech(input="Hello")
    result = json.loads(response)
    assert "error" in result


@pytest.mark.asyncio
async def test_openai_text_to_speech_handles_auth_error(monkeypatch):
    """Auth errors must be returned as a JSON error object."""
    from core.exceptions import OpenAIAuthError

    async def mock_audio_speech(**_kwargs):
        raise OpenAIAuthError("Invalid token")

    monkeypatch.setattr(audio_tools.client, "audio_speech", mock_audio_speech)

    response = await audio_tools.openai_text_to_speech(input="Hello")
    result = json.loads(response)
    assert result["error"] == "Authentication Error"
    assert "Invalid token" in result["message"]


@pytest.mark.asyncio
async def test_openai_text_to_speech_handles_api_error(monkeypatch):
    """API errors must be returned as a JSON error object."""
    from core.exceptions import OpenAIAPIError

    async def mock_audio_speech(**_kwargs):
        raise OpenAIAPIError(message="Service unavailable")

    monkeypatch.setattr(audio_tools.client, "audio_speech", mock_audio_speech)

    response = await audio_tools.openai_text_to_speech(input="Hello")
    result = json.loads(response)
    assert result["error"] == "API Error"
    assert "Service unavailable" in result["message"]
