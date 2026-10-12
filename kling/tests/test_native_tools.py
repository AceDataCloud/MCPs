from unittest.mock import AsyncMock, patch

import pytest
from pydantic import ValidationError

from core.native_types import (
    ApparelRequest,
    CommerceRequest,
    GoodsRequest,
    StoryboardRequest,
    TryOnRequest,
    TurboRequest,
)
from tools.native_tools import (
    kling_apparel_video,
    kling_generate_storyboard,
    kling_generate_turbo_video,
    kling_goods_studio,
    kling_video_commerce,
    kling_virtual_try_on,
)


@pytest.mark.parametrize(
    "tool,payload_model,path",
    [
        (
            kling_apparel_video,
            ApparelRequest(
                contents=[
                    {"type": "product_info", "text": "shirt"},
                    {"type": "source_video", "url": "https://example.com/v.mp4"},
                    {"type": "product_image", "url": "https://example.com/p.png"},
                ]
            ),
            "/kling/apparel",
        ),
        (
            kling_goods_studio,
            GoodsRequest(
                contents=[
                    {"type": "ref_image", "url": "https://example.com/p.png"},
                    {"type": "goods_title", "text": "shirt"},
                ],
                settings={"aspect_ratio": "1:1", "duration": 15},
            ),
            "/kling/goods-studio",
        ),
        (
            kling_video_commerce,
            CommerceRequest(
                contents=[
                    {"type": "avatar_id", "text": "avatar_anna_female"},
                    {"type": "speech_script", "text": "Hello"},
                ],
                settings={"bgm_enabled": False},
            ),
            "/kling/video-commerce",
        ),
        (
            kling_virtual_try_on,
            TryOnRequest(
                contents=[
                    {"type": "product_image", "url": "https://example.com/p.png"},
                    {"type": "person_image", "url": "https://example.com/person.png"},
                ],
                settings={"keep_face": False},
            ),
            "/kling/virtual-try-on",
        ),
    ],
)
async def test_commerce_request_exact_routes(tool, payload_model, path):
    with patch(
        "tools.native_tools.client.request", new=AsyncMock(return_value={"task_id": "platform"})
    ) as call:
        await tool(payload_model)
    assert call.await_args.args == (
        path,
        payload_model.model_dump(mode="json", by_alias=True, exclude_none=True),
    )


@pytest.mark.parametrize(
    "tool,payload_model",
    [
        (kling_generate_turbo_video, TurboRequest(prompt="ocean", duration=7)),
        (
            kling_generate_storyboard,
            StoryboardRequest(
                shot_type="customize",
                duration=5,
                multi_prompt=[
                    {"index": 1, "prompt": "ocean", "duration": 2},
                    {"index": 2, "prompt": "beach", "duration": 3},
                ],
            ),
        ),
    ],
)
async def test_native_video_request(tool, payload_model):
    with patch(
        "tools.native_tools.client.generate_video",
        new=AsyncMock(return_value={"task_id": "platform"}),
    ) as call:
        await tool(payload_model)
    assert call.await_args.kwargs == payload_model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )


@pytest.mark.parametrize(
    "body",
    [
        {"prompt": "x", "generate_audio": False},
        {"prompt": "x", "cfg_scale": 0.5},
        {"prompt": "x", "mode": "4k"},
    ],
)
def test_turbo_unsupported_controls_rejected(body):
    with pytest.raises(ValidationError):
        TurboRequest(**body)


def test_shot_duration_mismatch_rejected():
    with pytest.raises(ValidationError):
        StoryboardRequest(
            shot_type="customize",
            duration=5,
            multi_prompt=[{"index": 1, "prompt": "ocean", "duration": 2}],
        )
