"""Unit tests for motion transfer tools."""

import json
from unittest.mock import AsyncMock, patch

import pytest


@pytest.fixture
def mock_client_motion(mock_motion_response):
    with patch("tools.motion_tools.client") as mock_client:
        mock_client.generate_motion = AsyncMock(return_value=mock_motion_response)
        yield mock_client


class TestKlingGenerateMotion:
    """Tests for kling_generate_motion tool."""

    @pytest.mark.asyncio
    async def test_basic_motion_generation(self, mock_client_motion):
        from tools.motion_tools import kling_generate_motion

        result = await kling_generate_motion(
            image_url="https://example.com/character.jpg",
            video_url="https://example.com/motion.mp4",
        )
        data = json.loads(result)
        assert data["task_id"] == "test-motion-123"

        _, kwargs = mock_client_motion.generate_motion.call_args
        assert kwargs["image_url"] == "https://example.com/character.jpg"
        assert kwargs["video_url"] == "https://example.com/motion.mp4"
        assert "model_name" not in kwargs

    @pytest.mark.asyncio
    async def test_model_name_included_when_specified(self, mock_client_motion):
        from tools.motion_tools import kling_generate_motion

        await kling_generate_motion(
            image_url="https://example.com/character.jpg",
            video_url="https://example.com/motion.mp4",
            model_name="kling-v3",
        )

        _, kwargs = mock_client_motion.generate_motion.call_args
        assert kwargs["model_name"] == "kling-v3"

    @pytest.mark.asyncio
    async def test_model_name_v2_6(self, mock_client_motion):
        from tools.motion_tools import kling_generate_motion

        await kling_generate_motion(
            image_url="https://example.com/character.jpg",
            video_url="https://example.com/motion.mp4",
            model_name="kling-v2-6",
        )

        _, kwargs = mock_client_motion.generate_motion.call_args
        assert kwargs["model_name"] == "kling-v2-6"

    @pytest.mark.asyncio
    async def test_model_name_omitted_when_none(self, mock_client_motion):
        from tools.motion_tools import kling_generate_motion

        await kling_generate_motion(
            image_url="https://example.com/character.jpg",
            video_url="https://example.com/motion.mp4",
            model_name=None,
        )

        _, kwargs = mock_client_motion.generate_motion.call_args
        assert "model_name" not in kwargs

    @pytest.mark.asyncio
    async def test_mode_and_orientation_passed(self, mock_client_motion):
        from tools.motion_tools import kling_generate_motion

        await kling_generate_motion(
            image_url="https://example.com/character.jpg",
            video_url="https://example.com/motion.mp4",
            model_name="kling-v3",
            mode="pro",
            character_orientation="video",
        )

        _, kwargs = mock_client_motion.generate_motion.call_args
        assert kwargs["mode"] == "pro"
        assert kwargs["character_orientation"] == "video"
        assert kwargs["model_name"] == "kling-v3"
