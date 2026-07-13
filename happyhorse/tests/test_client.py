"""HTTP contract tests for the Happy Horse client."""

import httpx
import pytest
import respx

from core.client import HappyHorseClient
from core.exceptions import HappyHorseAPIError, HappyHorseAuthError, HappyHorseTimeoutError


@respx.mock
async def test_generation_uses_public_endpoint_and_defaults_async(api_token: str) -> None:
    route = respx.post("https://api.acedata.cloud/happyhorse/videos").mock(
        return_value=httpx.Response(200, json={"task_id": "task-1"})
    )

    result = await HappyHorseClient(api_token=api_token).generate_video(
        {"action": "generate", "prompt": "A horse at sunrise"}
    )

    assert result["task_id"] == "task-1"
    request = route.calls.last.request
    assert request.headers["authorization"] == "Bearer test-token"
    assert request.read() == (b'{"action":"generate","prompt":"A horse at sunrise","async":true}')


@respx.mock
async def test_callback_submission_does_not_add_async(api_token: str) -> None:
    route = respx.post("https://api.acedata.cloud/happyhorse/videos").mock(
        return_value=httpx.Response(200, json={"task_id": "task-1"})
    )

    await HappyHorseClient(api_token=api_token).generate_video(
        {"action": "generate", "callback_url": "https://example.com/callback"}
    )

    assert route.calls.last.request.read() == (
        b'{"action":"generate","callback_url":"https://example.com/callback"}'
    )


@respx.mock
async def test_task_operations_use_tasks_endpoint(api_token: str) -> None:
    route = respx.post("https://api.acedata.cloud/happyhorse/tasks").mock(
        side_effect=[
            httpx.Response(200, json={"id": "task-1"}),
            httpx.Response(200, json={"items": [], "count": 0}),
        ]
    )
    client = HappyHorseClient(api_token=api_token)

    await client.get_task("task-1")
    await client.get_tasks_batch(["task-1", "task-2"])

    assert route.calls[0].request.read() == b'{"id":"task-1","action":"retrieve"}'
    assert route.calls[1].request.read() == (
        b'{"ids":["task-1","task-2"],"action":"retrieve_batch"}'
    )


@respx.mock
async def test_403_remains_api_error(api_token: str) -> None:
    respx.post("https://api.acedata.cloud/happyhorse/videos").mock(
        return_value=httpx.Response(403, json={"detail": "content rejected"})
    )

    with pytest.raises(HappyHorseAPIError, match="content rejected") as exc_info:
        await HappyHorseClient(api_token=api_token).generate_video({"action": "generate"})

    assert exc_info.value.status_code == 403


async def test_missing_token_is_auth_error() -> None:
    with pytest.raises(HappyHorseAuthError, match="not configured"):
        await HappyHorseClient(api_token="").get_task("task-1")


@respx.mock
async def test_timeout_is_typed(api_token: str) -> None:
    respx.post("https://api.acedata.cloud/happyhorse/tasks").mock(
        side_effect=httpx.ReadTimeout("slow")
    )

    with pytest.raises(HappyHorseTimeoutError):
        await HappyHorseClient(api_token=api_token).get_task("task-1")
