from unittest.mock import AsyncMock, patch

import pytest
from pydantic import ValidationError

from core.asset_types import AssetManagementRequest, AssetVideoRequest, VoiceCreationRequest
from tools.asset_tools import kling_generate_with_assets, kling_manage_elements, kling_manage_voices


@pytest.mark.parametrize(
    "tool,payload_model,path",
    [
        (
            kling_manage_elements,
            AssetManagementRequest(action="presets", page_num=2),
            "/kling/elements",
        ),
        (
            kling_manage_voices,
            VoiceCreationRequest(voice_name="Narrator", voice_url="https://example.com/v.mp3"),
            "/kling/voices",
        ),
    ],
)
async def test_asset_management_route(tool, payload_model, path):
    with patch(
        "tools.asset_tools.client.request", new=AsyncMock(return_value={"task_id": "platform"})
    ) as call:
        await tool(payload_model)
    assert call.await_args.args == (
        path,
        payload_model.model_dump(mode="json", by_alias=True, exclude_none=True),
    )


async def test_voice_reference_ids_are_platform_ids():
    body = AssetVideoRequest(
        model="kling-v2-6",
        mode="pro",
        generate_audio=True,
        prompt="Hello <<<voice_1>>>",
        voice_list=[{"voice_id": "owned-platform-id"}],
    )
    with patch(
        "tools.asset_tools.client.generate_video",
        new=AsyncMock(return_value={"task_id": "platform"}),
    ) as call:
        await kling_generate_with_assets(body)
    assert call.await_args.kwargs["voice_list"] == [{"voice_id": "owned-platform-id"}]


@pytest.mark.parametrize("body", [{"action": "create"}, {"action": "delete"}, {"page_size": 501}])
def test_element_create_and_invalid_management_not_exposed(body):
    with pytest.raises(ValidationError):
        AssetManagementRequest(**body)


def test_voice_indices_must_match_selected_list():
    with pytest.raises(ValidationError):
        AssetVideoRequest(
            model="kling-v2-6",
            mode="pro",
            generate_audio=True,
            prompt="Hello <<<voice_2>>>",
            voice_list=[{"voice_id": "owned"}],
        )
