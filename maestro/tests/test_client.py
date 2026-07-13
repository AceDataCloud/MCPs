"""HTTP contract tests for the Maestro client."""

import httpx
import pytest
import respx

from core.client import MaestroClient
from core.exceptions import MaestroAPIError, MaestroAuthError, MaestroTimeoutError


@respx.mock
async def test_create_video_uses_public_endpoint(api_token: str) -> None:
    route = respx.post("https://api.acedata.cloud/maestro/videos").mock(
        return_value=httpx.Response(201, json={"success": True, "task_id": "task-1"})
    )
    client = MaestroClient(api_token=api_token)

    result = await client.create_video({"prompt": "Make a product video", "duration": 30})

    assert result["task_id"] == "task-1"
    request = route.calls.last.request
    assert request.headers["authorization"] == "Bearer test-token"
    assert request.read() == b'{"prompt":"Make a product video","duration":30}'


@respx.mock
async def test_task_operations_use_tasks_endpoint(api_token: str) -> None:
    route = respx.post("https://api.acedata.cloud/maestro/tasks").mock(
        side_effect=[
            httpx.Response(200, json={"id": "task-1", "status": "producing"}),
            httpx.Response(200, json={"count": 1, "items": []}),
        ]
    )
    client = MaestroClient(api_token=api_token)

    await client.get_task("task-1")
    await client.list_tasks(10, created_at_min=100, created_at_max=200)

    assert route.calls[0].request.read() == b'{"id":"task-1","action":"retrieve"}'
    assert route.calls[1].request.read() == (
        b'{"action":"retrieve_batch","limit":10,"created_at_min":100,"created_at_max":200}'
    )


@respx.mock
async def test_api_error_preserves_status(api_token: str) -> None:
    respx.post("https://api.acedata.cloud/maestro/tasks").mock(
        return_value=httpx.Response(404, json={"detail": "task not found"})
    )

    with pytest.raises(MaestroAPIError, match="task not found") as exc_info:
        await MaestroClient(api_token=api_token).get_task("missing")

    assert exc_info.value.status_code == 404


async def test_missing_token_is_auth_error() -> None:
    with pytest.raises(MaestroAuthError, match="not configured"):
        await MaestroClient(api_token="").get_task("task-1")


@respx.mock
async def test_timeout_is_typed(api_token: str) -> None:
    respx.post("https://api.acedata.cloud/maestro/tasks").mock(
        side_effect=httpx.ReadTimeout("slow")
    )

    with pytest.raises(MaestroTimeoutError):
        await MaestroClient(api_token=api_token).get_task("task-1")
