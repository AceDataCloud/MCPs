from unittest.mock import AsyncMock, patch

import pytest
from pydantic import ValidationError

from core.native_types import (
    BaseVideoRegenerationRequest,
    MaxVideoRequest,
    PromptEnhancementRequest,
    SourceRegenerationRequest,
)
from tools.native_tools import (
    minimax_enhance_prompt,
    minimax_generate_max_video,
    minimax_regenerate_video,
)


@pytest.mark.parametrize(
    "tool,payload_model,path",
    [
        (
            minimax_generate_max_video,
            MaxVideoRequest(
                content=[{"type": "text", "text": "ocean"}], resolution="480P", **{"async": False}
            ),
            "/minimax/videos",
        ),
        (
            minimax_enhance_prompt,
            PromptEnhancementRequest(content=[{"type": "text", "text": "ocean"}]),
            "/minimax/prompt-enhancement",
        ),
        (
            minimax_regenerate_video,
            SourceRegenerationRequest(source_task_id="owned", aigc_watermark=False),
            "/minimax/regenerate",
        ),
    ],
)
async def test_native_request_routes(tool, payload_model, path):
    with patch(
        "tools.native_tools.client.request", new=AsyncMock(return_value={"task_id": "platform"})
    ) as call:
        await tool(payload_model)
    assert call.await_args.args[0] == path
    assert call.await_args.args[1] == payload_model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )


@pytest.mark.parametrize("kwargs", [{"resolution": "2K"}, {"duration": 4}, {"model": "MiniMax-H3"}])
def test_max_disallows_legacy_only_combinations(kwargs):
    with pytest.raises(ValidationError):
        MaxVideoRequest(content=[{"type": "text", "text": "ocean"}], **kwargs)


def test_regeneration_never_accepts_upstream_task_id():
    with pytest.raises(ValidationError):
        SourceRegenerationRequest(source_task_id="owned", task_id="upstream")


async def test_original_material_regeneration_form():
    body = BaseVideoRegenerationRequest(
        content=[
            {"type": "text", "text": "original prompt"},
            {
                "type": "video_url",
                "role": "base_video",
                "video_url": {"url": "https://example.com/original.mp4"},
            },
        ]
    )
    with patch(
        "tools.native_tools.client.request", new=AsyncMock(return_value={"task_id": "platform"})
    ) as call:
        await minimax_regenerate_video(body)
    assert "source_task_id" not in call.await_args.args[1]
    assert call.await_args.args[1]["content"][1]["role"] == "base_video"
