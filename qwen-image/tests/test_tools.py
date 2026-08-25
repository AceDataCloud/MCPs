from unittest.mock import AsyncMock, patch

import pytest

from tools.image_tools import qwen_image_edit, qwen_image_generate


@pytest.mark.asyncio
async def test_generate_payload() -> None:
    with patch(
        "tools.image_tools.client.generate_image", new=AsyncMock(return_value={"task_id": "t"})
    ) as call:
        await qwen_image_generate("cat", n=2, size="1024*1024", seed=7)
        payload = call.call_args.kwargs
        assert payload["model"] == "qwen-image-3.0" and payload["n"] == 2 and payload["seed"] == 7


@pytest.mark.asyncio
async def test_edit_payload() -> None:
    with patch(
        "tools.image_tools.client.generate_image", new=AsyncMock(return_value={"task_id": "t"})
    ) as call:
        await qwen_image_edit(
            "restyle",
            ["https://example.com/a.png"],
            model="qwen-image-3.0-pro",
            prompt_extend_mode="agent",
        )
        payload = call.call_args.kwargs
        assert payload["image_urls"] == ["https://example.com/a.png"]
        assert payload["prompt_extend_mode"] == "agent"
