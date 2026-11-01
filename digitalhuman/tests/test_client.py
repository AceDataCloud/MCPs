"""HTTP contract tests for the Digital Human client."""

import httpx
import pytest
import respx

from core.client import DigitalHumanClient
from core.exceptions import DigitalHumanAPIError, DigitalHumanAuthError, DigitalHumanTimeoutError


@respx.mock
async def test_video_requests_use_videos_endpoint(api_token: str) -> None:
    route = respx.post("https://api.acedata.cloud/digital-human/videos").mock(
        return_value=httpx.Response(200, json={"task_id": "task-1"})
    )

    result = await DigitalHumanClient(api_token=api_token).create_video(
        {"video_url": "https://example.com/face.mp4", "audio_url": "https://example.com/voice.mp3"}
    )

    assert result["task_id"] == "task-1"
    request = route.calls.last.request
    assert request.headers["authorization"].startswith("Bearer ")
    assert request.headers["authorization"].endswith(api_token)
    assert request.read() == (
        b'{"video_url":"https://example.com/face.mp4","audio_url":"https://example.com/voice.mp3"}'
    )


@respx.mock
async def test_voice_requests_use_voices_endpoint(api_token: str) -> None:
    route = respx.post("https://api.acedata.cloud/digital-human/voices").mock(
        return_value=httpx.Response(200, json={"voice_id": "voice-1", "state": "succeed"})
    )

    result = await DigitalHumanClient(api_token=api_token).clone_voice(
        {"audio_url": "https://example.com/sample.wav", "lang": "en"}
    )

    assert result["voice_id"] == "voice-1"
    assert route.calls.last.request.read() == (
        b'{"audio_url":"https://example.com/sample.wav","lang":"en"}'
    )


@respx.mock
async def test_task_operations_use_exact_ids_instead_of_recent_history(api_token: str) -> None:
    import json

    async def retrieve(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        # The real retrieve_batch endpoint ignores IDs and returns recent history.
        if body["action"] == "retrieve_batch":
            return httpx.Response(200, json={"items": [{"id": "unrelated-recent"}]})
        if body["action"] == "delete":
            return httpx.Response(200, json={"id": body["task_id"], "deleted": True})
        return httpx.Response(200, json={"id": body["task_id"], "state": "succeeded"})

    route = respx.post("https://api.acedata.cloud/digital-human/tasks").mock(side_effect=retrieve)
    client = DigitalHumanClient(api_token=api_token)
    result = await client.get_tasks_batch(["older-task", "newer-task"])
    await client.delete_task("task-3")

    assert result == {
        "count": 2,
        "items": [
            {"id": "older-task", "state": "succeeded"},
            {"id": "newer-task", "state": "succeeded"},
        ],
    }
    assert [json.loads(call.request.content) for call in route.calls] == [
        {"task_id": "older-task", "action": "retrieve"},
        {"task_id": "newer-task", "action": "retrieve"},
        {"task_id": "task-3", "action": "delete"},
    ]
    assert all(
        call.request.headers["authorization"] == "Bearer " + api_token for call in route.calls
    )


@respx.mock
async def test_401_is_auth_error(api_token: str) -> None:
    respx.post("https://api.acedata.cloud/digital-human/videos").mock(
        return_value=httpx.Response(401, json={"error": {"message": "bad token"}})
    )

    with pytest.raises(DigitalHumanAuthError, match="bad token"):
        await DigitalHumanClient(api_token=api_token).create_video({"audio_url": "x"})


@respx.mock
async def test_timeout_is_typed(api_token: str) -> None:
    respx.post("https://api.acedata.cloud/digital-human/tasks").mock(
        side_effect=httpx.ReadTimeout("slow")
    )

    with pytest.raises(DigitalHumanTimeoutError):
        await DigitalHumanClient(api_token=api_token).get_task("task-1")


@respx.mock
async def test_non_auth_error_is_api_error(api_token: str) -> None:
    respx.post("https://api.acedata.cloud/digital-human/voices").mock(
        return_value=httpx.Response(500, json={"error": {"message": "voice clone failed"}})
    )

    with pytest.raises(DigitalHumanAPIError, match="voice clone failed") as exc_info:
        await DigitalHumanClient(api_token=api_token).clone_voice(
            {"audio_url": "https://example.com/sample.wav"}
        )

    assert exc_info.value.status_code == 500
