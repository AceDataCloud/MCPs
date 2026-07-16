"""Unit tests for video generation tools."""

from unittest.mock import AsyncMock, patch

import pytest

from core.types import (
    KlingCameraControl,
    KlingCameraControlConfig,
    KlingReferenceImage,
    KlingReferenceVideo,
)


@pytest.fixture
def mock_client_generate_video(mock_video_response):
    """Patch client.generate_video with a mock that returns a canned response."""
    with patch("tools.video_tools.client") as mock_client:
        mock_client.generate_video = AsyncMock(return_value=mock_video_response)
        yield mock_client


class TestKlingGenerateVideo:
    """Tests for kling_generate_video tool."""

    @pytest.mark.asyncio
    async def test_image_list_included_in_canonical_o1_payload(self, mock_client_generate_video):
        from tools.video_tools import kling_generate_video

        image_list = [KlingReferenceImage(image_url="https://example.com/ref.jpg")]
        await kling_generate_video(
            prompt="Animate <<<image_1>>>",
            model="kling-o1",
            duration=5,
            image_list=image_list,
        )

        _, kwargs = mock_client_generate_video.generate_video.call_args
        assert kwargs["model"] == "kling-o1"
        assert kwargs["image_list"] == [{"image_url": "https://example.com/ref.jpg"}]

    @pytest.mark.asyncio
    async def test_reference_lists_omitted_when_none(self, mock_client_generate_video):
        from tools.video_tools import kling_generate_video

        await kling_generate_video(prompt="A test video")

        _, kwargs = mock_client_generate_video.generate_video.call_args
        assert "image_list" not in kwargs
        assert "video_list" not in kwargs

    @pytest.mark.asyncio
    async def test_video_list_included_in_v3_omni_payload(self, mock_client_generate_video):
        from tools.video_tools import kling_generate_video

        video_list = [
            KlingReferenceVideo(
                video_url="https://example.com/ref.mp4",
                refer_type="feature",
                keep_original_sound="yes",
            )
        ]
        await kling_generate_video(
            prompt="Continue from <<<video_1>>>",
            model="kling-v3-omni",
            video_list=video_list,
        )

        _, kwargs = mock_client_generate_video.generate_video.call_args
        assert kwargs["video_list"] == [
            {
                "video_url": "https://example.com/ref.mp4",
                "refer_type": "feature",
                "keep_original_sound": "yes",
            }
        ]

    @pytest.mark.asyncio
    async def test_non_omni_model_rejects_references(self, mock_client_generate_video):
        from tools.video_tools import kling_generate_video

        result = await kling_generate_video(
            prompt="A test video",
            model="kling-v2-master",
            image_list=[KlingReferenceImage(image_url="https://example.com/ref.jpg")],
        )

        assert result == "Error: image_list and video_list are not supported by kling-v2-master."
        mock_client_generate_video.generate_video.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_o1_rejects_unsupported_duration(self, mock_client_generate_video):
        from tools.video_tools import kling_generate_video

        result = await kling_generate_video(prompt="A test video", model="kling-o1", duration=10)

        assert result == "Error: kling-o1 supports duration=5 only."
        mock_client_generate_video.generate_video.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_v3_rejects_duration_outside_range(self, mock_client_generate_video):
        from tools.video_tools import kling_generate_video

        result = await kling_generate_video(prompt="A test video", model="kling-v3", duration=16)

        assert result == "Error: kling-v3 duration must be an integer from 3 to 15."
        mock_client_generate_video.generate_video.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_omni_references_reject_4k(self, mock_client_generate_video):
        from tools.video_tools import kling_generate_video

        result = await kling_generate_video(
            prompt="Use <<<image_1>>>",
            model="kling-v3-omni",
            mode="4k",
            image_list=[KlingReferenceImage(image_url="https://example.com/ref.jpg")],
        )

        assert result == "Error: mode=4k is not supported with image_list or video_list."
        mock_client_generate_video.generate_video.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_reference_video_limits_images_to_four(self, mock_client_generate_video):
        from tools.video_tools import kling_generate_video

        result = await kling_generate_video(
            prompt="Use references",
            model="kling-v3-omni",
            image_list=[
                KlingReferenceImage(image_url=f"https://example.com/ref-{index}.jpg")
                for index in range(5)
            ],
            video_list=[KlingReferenceVideo(video_url="https://example.com/ref.mp4")],
        )

        assert (
            result
            == "Error: this request supports at most 4 reference images including first/end frames."
        )
        mock_client_generate_video.generate_video.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_structured_camera_control_is_serialized(self, mock_client_generate_video):
        from tools.video_tools import kling_generate_video

        await kling_generate_video(
            prompt="Pan left",
            model="kling-v3",
            camera_control=KlingCameraControl(
                type="simple",
                config=KlingCameraControlConfig(horizontal=-0.5),
            ),
        )

        _, kwargs = mock_client_generate_video.generate_video.call_args
        assert kwargs["camera_control"] == {
            "type": "simple",
            "config": {"horizontal": -0.5},
        }


class TestKlingGenerateVideoFromImage:
    """Tests for kling_generate_video_from_image tool."""

    @pytest.mark.asyncio
    async def test_start_image_is_required(self, mock_client_generate_video):
        from tools.video_tools import kling_generate_video_from_image

        result = await kling_generate_video_from_image(
            prompt="Animate this image",
            end_image_url="https://example.com/end.jpg",
        )

        assert result == "Error: start_image_url is required for image-to-video generation."
        mock_client_generate_video.generate_video.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_duplicate_first_frame_sources_are_rejected(self, mock_client_generate_video):
        from tools.video_tools import kling_generate_video_from_image

        result = await kling_generate_video_from_image(
            prompt="Animate this image",
            start_image_url="https://example.com/start.jpg",
            model="kling-v3-omni",
            image_list=[
                KlingReferenceImage(
                    image_url="https://example.com/other-start.jpg",
                    type="first_frame",
                )
            ],
        )

        assert result == "Error: provide at most one first frame and one end frame."
        mock_client_generate_video.generate_video.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_feature_video_can_accompany_start_frame(self, mock_client_generate_video):
        from tools.video_tools import kling_generate_video_from_image

        video_list = [
            KlingReferenceVideo(video_url="https://example.com/ref.mp4", refer_type="feature")
        ]
        await kling_generate_video_from_image(
            prompt="Animate this image",
            start_image_url="https://example.com/start.jpg",
            model="kling-v3-omni",
            video_list=video_list,
        )

        _, kwargs = mock_client_generate_video.generate_video.call_args
        assert kwargs["start_image_url"] == "https://example.com/start.jpg"
        assert kwargs["video_list"][0]["refer_type"] == "feature"

    @pytest.mark.asyncio
    async def test_base_video_rejects_start_frame(self, mock_client_generate_video):
        from tools.video_tools import kling_generate_video_from_image

        result = await kling_generate_video_from_image(
            prompt="Animate this image",
            start_image_url="https://example.com/start.jpg",
            model="kling-o1",
            video_list=[
                KlingReferenceVideo(video_url="https://example.com/ref.mp4", refer_type="base")
            ],
        )

        assert (
            result == "Error: an editable base video cannot be combined with first or end frames."
        )
        mock_client_generate_video.generate_video.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_reference_lists_omitted_when_none(self, mock_client_generate_video):
        from tools.video_tools import kling_generate_video_from_image

        await kling_generate_video_from_image(
            prompt="Animate this image",
            start_image_url="https://example.com/start.jpg",
        )

        _, kwargs = mock_client_generate_video.generate_video.call_args
        assert "image_list" not in kwargs
        assert "video_list" not in kwargs


class TestKlingExtendVideo:
    """Tests for kling_extend_video tool validation."""

    @pytest.mark.asyncio
    async def test_o1_extend_is_rejected(self, mock_client_generate_video):
        from tools.video_tools import kling_extend_video

        result = await kling_extend_video(video_id="video-id", prompt="Continue", model="kling-o1")

        assert result == "Error: action=extend is not supported by kling-o1."
        mock_client_generate_video.generate_video.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_invalid_legacy_duration_is_rejected(self, mock_client_generate_video):
        from tools.video_tools import kling_extend_video

        result = await kling_extend_video(
            video_id="video-id",
            prompt="Continue",
            model="kling-v2-master",
            duration=7,
        )

        assert result == "Error: kling-v2-master duration must be 5 or 10."
        mock_client_generate_video.generate_video.assert_not_awaited()
