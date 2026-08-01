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
async def test_task_operations_use_tasks_endpoint(api_token: str) -> None:
    route = respx.post("https://api.acedata.cloud/digital-human/tasks").mock(
        side_effect=[
            httpx.Response(200, json={"task_id": "task-1", "state": "processing"}),
            httpx.Response(200, json={"items": [], "count": 0}),
            httpx.Response(200, json={"success": True}),
        ]
    )
    client = DigitalHumanClient(api_token=api_token)

    await client.get_task("task-1", action="retrieve")
    await client.get_tasks_batch(["task-1", "task-2"])
    await client.delete_task("task-3")

    assert route.calls[0].request.read() == b'{"task_id":"task-1","action":"retrieve"}'
    assert route.calls[1].request.read() == (
        b'{"task_id":["task-1","task-2"],"action":"retrieve_batch"}'
    )
    assert route.calls[2].request.read() == b'{"task_id":"task-3","action":"delete"}'


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
