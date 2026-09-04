"""Unit tests for style tools."""

from unittest.mock import AsyncMock, patch

import pytest

from tools.style_tools import suno_create_voice, suno_upload_audio


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


class TestUploadAudioTool:
    @pytest.mark.asyncio
    async def test_optional_fields_are_omitted_by_default(self):
        with patch(
            "tools.style_tools.client.upload_audio",
            new=AsyncMock(return_value={"success": True}),
        ) as mock_upload_audio:
            await suno_upload_audio(audio_url="https://example.com/source.mp3")

        assert mock_upload_audio.await_args.kwargs == {
            "audio_url": "https://example.com/source.mp3",
        }

    @pytest.mark.asyncio
    async def test_mode_and_callback_are_forwarded_when_provided(self):
        with patch(
            "tools.style_tools.client.upload_audio",
            new=AsyncMock(return_value={"success": True}),
        ) as mock_upload_audio:
            await suno_upload_audio(
                audio_url="https://example.com/source.mp3",
                mode="enhanced",
                callback_url="https://example.com/webhook",
            )

        assert mock_upload_audio.await_args.kwargs == {
            "audio_url": "https://example.com/source.mp3",
            "mode": "enhanced",
            "callback_url": "https://example.com/webhook",
        }
