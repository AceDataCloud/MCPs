"""Unit tests for video generation tools."""

from unittest.mock import AsyncMock, patch

import pytest


@pytest.fixture
def mock_client_generate_video(mock_video_response):
    """Patch client.generate_video with a mock that returns a canned response."""
    with patch("tools.video_tools.client") as mock_client:
        mock_client.generate_video = AsyncMock(return_value=mock_video_response)
        yield mock_client


class TestKlingGenerateVideo:
    """Tests for kling_generate_video tool."""

    @pytest.mark.asyncio
    async def test_element_list_included_in_payload(self, mock_client_generate_video):
        """Test that element_list is forwarded to the API when provided."""
        from tools.video_tools import kling_generate_video

        element_list = [{"element_id": "elem-001"}, {"element_id": "elem-002"}]
        await kling_generate_video(
            prompt="A test video",
            element_list=element_list,
        )

        _, kwargs = mock_client_generate_video.generate_video.call_args
        assert kwargs.get("element_list") == element_list

    @pytest.mark.asyncio
    async def test_element_list_omitted_when_none(self, mock_client_generate_video):
        """Test that element_list is not included when not provided."""
        from tools.video_tools import kling_generate_video

        await kling_generate_video(prompt="A test video")

        _, kwargs = mock_client_generate_video.generate_video.call_args
        assert "element_list" not in kwargs

    @pytest.mark.asyncio
    async def test_video_list_included_in_payload(self, mock_client_generate_video):
        """Test that video_list is forwarded to the API when provided."""
        from tools.video_tools import kling_generate_video

        video_list = [{"video_url": "https://example.com/ref.mp4", "refer_type": "feature"}]
        await kling_generate_video(
            prompt="A test video",
            video_list=video_list,
        )

        _, kwargs = mock_client_generate_video.generate_video.call_args
        assert kwargs.get("video_list") == video_list

    @pytest.mark.asyncio
    async def test_video_list_omitted_when_none(self, mock_client_generate_video):
        """Test that video_list is not included when not provided."""
        from tools.video_tools import kling_generate_video

        await kling_generate_video(prompt="A test video")

        _, kwargs = mock_client_generate_video.generate_video.call_args
        assert "video_list" not in kwargs


class TestKlingGenerateVideoFromImage:
    """Tests for kling_generate_video_from_image tool."""

    @pytest.mark.asyncio
    async def test_element_list_included_in_payload(self, mock_client_generate_video):
        """Test that element_list is forwarded when using image2video."""
        from tools.video_tools import kling_generate_video_from_image

        element_list = [{"element_id": "elem-001"}]
        await kling_generate_video_from_image(
            prompt="Animate this image",
            start_image_url="https://example.com/start.jpg",
            element_list=element_list,
        )

        _, kwargs = mock_client_generate_video.generate_video.call_args
        assert kwargs.get("element_list") == element_list

    @pytest.mark.asyncio
    async def test_video_list_included_in_payload(self, mock_client_generate_video):
        """Test that video_list is forwarded when using image2video."""
        from tools.video_tools import kling_generate_video_from_image

        video_list = [{"video_url": "https://example.com/ref.mp4", "refer_type": "base"}]
        await kling_generate_video_from_image(
            prompt="Animate this image",
            start_image_url="https://example.com/start.jpg",
            video_list=video_list,
        )

        _, kwargs = mock_client_generate_video.generate_video.call_args
        assert kwargs.get("video_list") == video_list

    @pytest.mark.asyncio
    async def test_element_list_omitted_when_none(self, mock_client_generate_video):
        """Test that element_list is not included when not provided."""
        from tools.video_tools import kling_generate_video_from_image

        await kling_generate_video_from_image(
            prompt="Animate this image",
            start_image_url="https://example.com/start.jpg",
        )

        _, kwargs = mock_client_generate_video.generate_video.call_args
        assert "element_list" not in kwargs

    @pytest.mark.asyncio
    async def test_video_list_omitted_when_none(self, mock_client_generate_video):
        """Test that video_list is not included when not provided."""
        from tools.video_tools import kling_generate_video_from_image

        await kling_generate_video_from_image(
            prompt="Animate this image",
            start_image_url="https://example.com/start.jpg",
        )

        _, kwargs = mock_client_generate_video.generate_video.call_args
        assert "video_list" not in kwargs
