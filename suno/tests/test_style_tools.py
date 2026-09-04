"""Unit tests for style tools."""

from unittest.mock import AsyncMock, patch

import pytest

from tools.style_tools import suno_create_voice, suno_upload_enhanced_audio


class TestCreateVoiceTool:
    @pytest.mark.asyncio
    async def test_name_is_optional(self):
        with patch(
            "tools.style_tools.client.create_voice",
            new=AsyncMock(return_value={"success": True}),
        ) as mock_create_voice:
            await suno_create_voice(audio_url="https://example.com/voice.mp3")

        assert mock_create_voice.await_args.kwargs == {
            "audio_url": "https://example.com/voice.mp3",
        }


class TestEnhancedUploadTool:
    @pytest.mark.asyncio
    async def test_submits_required_fields_without_empty_callback(self):
        with patch(
            "tools.style_tools.client.upload_enhanced_audio",
            new=AsyncMock(return_value={"task_id": "task-1"}),
        ) as mock_upload:
            result = await suno_upload_enhanced_audio(
                audio_url="https://example.com/audio.mp3",
                name="My Song",
            )

        assert '"task_id": "task-1"' in result
        assert mock_upload.await_args.kwargs == {
            "audio_url": "https://example.com/audio.mp3",
            "name": "My Song",
        }

    @pytest.mark.asyncio
    async def test_forwards_callback_url(self):
        with patch(
            "tools.style_tools.client.upload_enhanced_audio",
            new=AsyncMock(return_value={"task_id": "task-1"}),
        ) as mock_upload:
            await suno_upload_enhanced_audio(
                audio_url="https://example.com/audio.mp3",
                name="My Song",
                callback_url="https://example.com/webhook",
            )

        assert mock_upload.await_args.kwargs["callback_url"] == "https://example.com/webhook"
