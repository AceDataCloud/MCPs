import pytest
import respx
from httpx import Response

from core.client import QwenImageClient
from core.exceptions import QwenImageAuthError


@pytest.mark.asyncio
@respx.mock
async def test_generation_uses_public_endpoint_and_defaults_async() -> None:
    route = respx.post("https://api.acedata.cloud/qwen-image/images").mock(
        return_value=Response(200, json={"task_id": "t1"})
    )
    result = await QwenImageClient(api_token="token").generate_image(
        model="qwen-image-3.0", prompt="cat"
    )
    assert result["task_id"] == "t1"
    assert route.calls[0].request.read()
    assert b'"async":true' in route.calls[0].request.content


@pytest.mark.asyncio
@respx.mock
async def test_tasks_use_public_endpoint() -> None:
    route = respx.post("https://api.acedata.cloud/qwen-image/tasks").mock(
        return_value=Response(200, json={"id": "t1"})
    )
    await QwenImageClient(api_token="token").query_task(id="t1", action="retrieve")
    assert route.called


@pytest.mark.asyncio
async def test_missing_token_fails() -> None:
    with pytest.raises(QwenImageAuthError):
        await QwenImageClient(api_token="").query_task(id="t1", action="retrieve")
