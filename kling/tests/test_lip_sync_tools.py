"""Unit tests for lip-sync and talking-photo tools."""

import json
from unittest.mock import AsyncMock, patch

import pytest


@pytest.fixture
def mock_lip_sync_response():
    """Mock successful lip-sync response."""
    return {
        "success": True,
        "task_id": "test-lipsync-123",
        "video_url": None,
        "state": "submitted",
    }


@pytest.fixture
def mock_talking_photo_response():
    """Mock successful talking-photo response."""
    return {
        "success": True,
        "task_id": "test-talkingphoto-456",
        "video_url": None,
        "state": "submitted",
    }


@pytest.fixture
def mock_client_lip_sync(mock_lip_sync_response):
    with patch("tools.lip_sync_tools.client") as mock_client:
        mock_client.lip_sync = AsyncMock(return_value=mock_lip_sync_response)
        yield mock_client


@pytest.fixture
def mock_client_talking_photo(mock_talking_photo_response):
    with patch("tools.lip_sync_tools.client") as mock_client:
        mock_client.talking_photo = AsyncMock(return_value=mock_talking_photo_response)
        yield mock_client


class TestKlingLipSync:
    """Tests for kling_lip_sync tool."""

    @pytest.mark.asyncio
    async def test_audio2video_with_url(self, mock_client_lip_sync):
        from tools.lip_sync_tools import kling_lip_sync

        result = await kling_lip_sync(
            mode="audio2video",
            video_url="https://example.com/video.mp4",
            audio_url="https://example.com/audio.mp3",
        )
        data = json.loads(result)
        assert data["task_id"] == "test-lipsync-123"

        _, kwargs = mock_client_lip_sync.lip_sync.call_args
        assert kwargs["mode"] == "audio2video"
        assert kwargs["video_url"] == "https://example.com/video.mp4"
        assert kwargs["audio_url"] == "https://example.com/audio.mp3"

    @pytest.mark.asyncio
    async def test_text2video_mode(self, mock_client_lip_sync):
        from tools.lip_sync_tools import kling_lip_sync

        result = await kling_lip_sync(
            mode="text2video",
            video_url="https://example.com/video.mp4",
            text="Hello, this is a test.",
            voice_language="en",
        )
        data = json.loads(result)
        assert data["task_id"] == "test-lipsync-123"

        _, kwargs = mock_client_lip_sync.lip_sync.call_args
        assert kwargs["mode"] == "text2video"
        assert kwargs["text"] == "Hello, this is a test."
        assert kwargs["voice_language"] == "en"

    @pytest.mark.asyncio
    async def test_missing_video_source_returns_error(self):
        from tools.lip_sync_tools import kling_lip_sync

        result = await kling_lip_sync(
            mode="audio2video",
            audio_url="https://example.com/audio.mp3",
        )
        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_audio2video_missing_audio_returns_error(self):
        from tools.lip_sync_tools import kling_lip_sync

        result = await kling_lip_sync(
            mode="audio2video",
            video_url="https://example.com/video.mp4",
        )
        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_text2video_missing_text_returns_error(self):
        from tools.lip_sync_tools import kling_lip_sync

        result = await kling_lip_sync(
            mode="text2video",
            video_url="https://example.com/video.mp4",
        )
        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_video_id_accepted(self, mock_client_lip_sync):
        from tools.lip_sync_tools import kling_lip_sync

        await kling_lip_sync(
            mode="audio2video",
            video_id="task-abc-123",
            audio_url="https://example.com/audio.mp3",
        )
        _, kwargs = mock_client_lip_sync.lip_sync.call_args
        assert kwargs["video_id"] == "task-abc-123"
        assert "video_url" not in kwargs


class TestKlingTalkingPhoto:
    """Tests for kling_talking_photo tool."""

    @pytest.mark.asyncio
    async def test_basic_talking_photo(self, mock_client_talking_photo):
        from tools.lip_sync_tools import kling_talking_photo

        result = await kling_talking_photo(
            image_url="https://example.com/portrait.jpg",
            audio_url="https://example.com/speech.mp3",
        )
        data = json.loads(result)
        assert data["task_id"] == "test-talkingphoto-456"

        _, kwargs = mock_client_talking_photo.talking_photo.call_args
        assert kwargs["image_url"] == "https://example.com/portrait.jpg"
        assert kwargs["audio_url"] == "https://example.com/speech.mp3"
        assert kwargs["model"] == "kling-v2-1-master"
        assert kwargs["duration"] == 5
        assert kwargs["mode"] == "pro"

    @pytest.mark.asyncio
    async def test_custom_model_and_duration(self, mock_client_talking_photo):
        from tools.lip_sync_tools import kling_talking_photo

        await kling_talking_photo(
            image_url="https://example.com/portrait.jpg",
            audio_url="https://example.com/speech.mp3",
            model="kling-v1-6",
            duration=10,
            mode="std",
        )
        _, kwargs = mock_client_talking_photo.talking_photo.call_args
        assert kwargs["model"] == "kling-v1-6"
        assert kwargs["duration"] == 10
        assert kwargs["mode"] == "std"

    @pytest.mark.asyncio
    async def test_prompt_included_when_provided(self, mock_client_talking_photo):
        from tools.lip_sync_tools import kling_talking_photo

        await kling_talking_photo(
            image_url="https://example.com/portrait.jpg",
            audio_url="https://example.com/speech.mp3",
            prompt="A professional presenter",
        )
        _, kwargs = mock_client_talking_photo.talking_photo.call_args
        assert kwargs["prompt"] == "A professional presenter"

    @pytest.mark.asyncio
    async def test_prompt_not_included_when_none(self, mock_client_talking_photo):
        from tools.lip_sync_tools import kling_talking_photo

        await kling_talking_photo(
            image_url="https://example.com/portrait.jpg",
            audio_url="https://example.com/speech.mp3",
        )
        _, kwargs = mock_client_talking_photo.talking_photo.call_args
        assert "prompt" not in kwargs
