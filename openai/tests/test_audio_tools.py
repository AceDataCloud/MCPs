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


# ---------------------------------------------------------------------------
# Tests for openai_transcribe_audio
# ---------------------------------------------------------------------------


def test_openai_transcribe_audio_registered():
    """The openai_transcribe_audio tool must be registered with the MCP server."""
    tool_names = [tool.name for tool in mcp._tool_manager.list_tools()]
    assert "openai_transcribe_audio" in tool_names


def test_openai_transcribe_audio_schema():
    """The MCP schema for openai_transcribe_audio must include all expected parameters."""
    tool = next(
        tool for tool in mcp._tool_manager.list_tools() if tool.name == "openai_transcribe_audio"
    )
    props = tool.parameters["properties"]
    assert "url" in props
    assert "model" in props
    assert "language" in props
    assert "prompt" in props
    assert "response_format" in props
    assert "temperature" in props
    assert "timestamp_granularities" in props
    assert "url" in tool.parameters.get("required", [])


@pytest.mark.asyncio
async def test_openai_transcribe_audio_returns_json(monkeypatch):
    """Tool must return JSON with transcribed text."""
    fake_audio = b"fake-audio-bytes"
    fake_transcription = {"text": "Hello from AceData Cloud."}

    class MockResponse:
        content = fake_audio
        status_code = 200

        def raise_for_status(self):
            pass

    class MockHttpxClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def get(self, _url, **_kwargs):
            return MockResponse()

    async def mock_audio_transcriptions(audio_bytes, **_kwargs):
        assert audio_bytes == fake_audio
        return fake_transcription

    monkeypatch.setattr(audio_tools.httpx, "AsyncClient", MockHttpxClient)
    monkeypatch.setattr(audio_tools.client, "audio_transcriptions", mock_audio_transcriptions)

    response = await audio_tools.openai_transcribe_audio(url="https://example.com/audio.mp3")

    result = json.loads(response)
    assert result["text"] == "Hello from AceData Cloud."


@pytest.mark.asyncio
async def test_openai_transcribe_audio_forwards_all_params(monkeypatch):
    """All optional parameters must be forwarded correctly to the client."""
    captured: dict = {}

    class MockResponse:
        content = b"audio"
        status_code = 200

        def raise_for_status(self):
            pass

    class MockHttpxClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def get(self, _url, **_kwargs):
            return MockResponse()

    async def mock_audio_transcriptions(_audio_bytes, **kwargs):
        captured.update(kwargs)
        return {"text": "Test"}

    monkeypatch.setattr(audio_tools.httpx, "AsyncClient", MockHttpxClient)
    monkeypatch.setattr(audio_tools.client, "audio_transcriptions", mock_audio_transcriptions)

    await audio_tools.openai_transcribe_audio(
        url="https://example.com/audio.mp3",
        model="whisper-1",
        language="en",
        prompt="Test hint",
        response_format="verbose_json",
        temperature=0.2,
        timestamp_granularities=["word"],
    )

    assert captured["model"] == "whisper-1"
    assert captured["language"] == "en"
    assert captured["prompt"] == "Test hint"
    assert captured["response_format"] == "verbose_json"
    assert captured["temperature"] == 0.2
    assert captured["timestamp_granularities"] == ["word"]


@pytest.mark.asyncio
async def test_openai_transcribe_audio_omits_none_params(monkeypatch):
    """Optional params must not be included in the payload when not provided."""
    captured: dict = {}

    class MockResponse:
        content = b"audio"
        status_code = 200

        def raise_for_status(self):
            pass

    class MockHttpxClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def get(self, _url, **_kwargs):
            return MockResponse()

    async def mock_audio_transcriptions(_audio_bytes, **kwargs):
        captured.update(kwargs)
        return {"text": "Result"}

    monkeypatch.setattr(audio_tools.httpx, "AsyncClient", MockHttpxClient)
    monkeypatch.setattr(audio_tools.client, "audio_transcriptions", mock_audio_transcriptions)

    await audio_tools.openai_transcribe_audio(url="https://example.com/audio.mp3")

    assert "language" not in captured
    assert "prompt" not in captured
    assert "temperature" not in captured
    assert "timestamp_granularities" not in captured


@pytest.mark.asyncio
async def test_openai_transcribe_audio_handles_empty_audio(monkeypatch):
    """Empty downloaded audio must return an error JSON."""

    class MockResponse:
        content = b""
        status_code = 200

        def raise_for_status(self):
            pass

    class MockHttpxClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def get(self, _url, **_kwargs):
            return MockResponse()

    monkeypatch.setattr(audio_tools.httpx, "AsyncClient", MockHttpxClient)

    response = await audio_tools.openai_transcribe_audio(url="https://example.com/empty.mp3")
    result = json.loads(response)
    assert "error" in result


@pytest.mark.asyncio
async def test_openai_transcribe_audio_handles_auth_error(monkeypatch):
    """Auth errors must be returned as a JSON error object."""
    from core.exceptions import OpenAIAuthError

    class MockResponse:
        content = b"audio"
        status_code = 200

        def raise_for_status(self):
            pass

    class MockHttpxClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def get(self, _url, **_kwargs):
            return MockResponse()

    async def mock_audio_transcriptions(_audio_bytes, **_kwargs):
        raise OpenAIAuthError("Invalid token")

    monkeypatch.setattr(audio_tools.httpx, "AsyncClient", MockHttpxClient)
    monkeypatch.setattr(audio_tools.client, "audio_transcriptions", mock_audio_transcriptions)

    response = await audio_tools.openai_transcribe_audio(url="https://example.com/audio.mp3")
    result = json.loads(response)
    assert result["error"] == "Authentication Error"
    assert "Invalid token" in result["message"]


@pytest.mark.asyncio
async def test_openai_transcribe_audio_handles_api_error(monkeypatch):
    """API errors must be returned as a JSON error object."""
    from core.exceptions import OpenAIAPIError

    class MockResponse:
        content = b"audio"
        status_code = 200

        def raise_for_status(self):
            pass

    class MockHttpxClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def get(self, _url, **_kwargs):
            return MockResponse()

    async def mock_audio_transcriptions(_audio_bytes, **_kwargs):
        raise OpenAIAPIError(message="Transcription failed")

    monkeypatch.setattr(audio_tools.httpx, "AsyncClient", MockHttpxClient)
    monkeypatch.setattr(audio_tools.client, "audio_transcriptions", mock_audio_transcriptions)

    response = await audio_tools.openai_transcribe_audio(url="https://example.com/audio.mp3")
    result = json.loads(response)
    assert result["error"] == "API Error"
    assert "Transcription failed" in result["message"]
