"""Project contracts: action schemas, idempotency headers and version preservation."""

import json
from unittest.mock import AsyncMock, patch

import httpx
import pytest
import respx
from pydantic import TypeAdapter, ValidationError

from core.client import SunoClient
from core.project_types import SunoProjectRequest
from core.server import mcp
from tools import project_tools  # noqa: F401
from tools.project_tools import suno_manage_project

PROJECT = {"id": "project-1", "version_id": "version-2"}
SECTION = {
    **PROJECT,
    "source_audio_id": "audio",
    "model": "chirp-v5-5",
    "start_seconds": 0,
    "end_seconds": 10,
}
CASES = [
    {"action": "create", "title": "Project"},
    {"action": "retrieve", "id": "project-1"},
    {"action": "save", **PROJECT, "state": {"tracks": [], "custom_metadata": {"keep": True}}},
    {"action": "upload", **PROJECT, "audio_url": "https://example.com/audio.wav"},
    {"action": "add_track", **PROJECT, "audio_id": "audio", "gain": 0, "start_beats": 0},
    {
        "action": "generate_track",
        **SECTION,
        "render_audio_id": "render",
        "stem_control_tags": "add Piano",
        "instrumental": False,
        "vocal_gender": "f",
    },
    {"action": "replace_section", **SECTION, "replacement_lyrics": "new words", "fixed": False},
    {
        "action": "commit_candidate",
        **PROJECT,
        "operation_id": "operation",
        "candidate_id": "candidate",
        "track_id": "track",
        "gain": 0,
    },
    {"action": "remove_track", **PROJECT, "track_id": "track"},
    {"action": "render", **PROJECT, "title": "Mix", "lyrics": "[Instrumental]"},
]


@pytest.mark.parametrize("case", CASES)
async def test_all_project_actions_dispatch_without_losing_public_fields(case):
    arguments = {"request": case}
    if case["action"] != "retrieve":
        arguments["idempotency_key"] = "stable-write-key"
    with patch(
        "tools.project_tools.client.manage_project", new=AsyncMock(return_value={"task_id": "task"})
    ) as call:
        await mcp.call_tool("suno_manage_project", arguments)
    payload = call.await_args.kwargs
    assert all(payload[k] == v for k, v in case.items())
    assert payload["idempotency_key"] == arguments.get("idempotency_key")
    assert "async_" not in payload
    if "async" in payload:
        assert payload["async"] is True


async def test_write_requires_explicit_idempotency_key_before_network():
    request = TypeAdapter(SunoProjectRequest).validate_python(CASES[0])
    with (
        patch("tools.project_tools.client.manage_project", new=AsyncMock()) as call,
        pytest.raises(ValueError, match="idempotency_key"),
    ):
        await suno_manage_project(request)
    call.assert_not_awaited()


@pytest.mark.parametrize(
    "case",
    [
        {"action": "render", "id": "project", "title": "Missing version"},
        {
            "action": "generate_track",
            **SECTION,
            "render_audio_id": "render",
            "stem_control_tags": "add Piano",
            "end_seconds": 0,
        },
        {"action": "replace_section", **SECTION, "fixed": True, "end_seconds": 26},
    ],
)
def test_invalid_version_or_source_range_rejected(case):
    with pytest.raises(ValidationError):
        TypeAdapter(SunoProjectRequest).validate_python(case)


async def test_completed_project_response_is_not_labeled_as_a_new_async_submission():
    request = TypeAdapter(SunoProjectRequest).validate_python(CASES[1])
    response = {
        "success": True,
        "task_id": "completed",
        "data": {"id": "project", "version_id": "latest"},
    }
    with patch("tools.project_tools.client.manage_project", new=AsyncMock(return_value=response)):
        result = json.loads(await suno_manage_project(request))
    assert result == response


@respx.mock
async def test_client_preserves_retry_key_as_header_and_does_not_change_version():
    route = respx.post("https://api.test.com/suno/projects").mock(
        return_value=httpx.Response(200, json={"task_id": "same-task"})
    )
    client = SunoClient(api_token="test-token", base_url="https://api.test.com")
    for _ in range(2):
        await client.manage_project(
            idempotency_key="same-key", action="render", **PROJECT, title="Mix", **{"async": True}
        )
    assert route.call_count == 2
    for call in route.calls:
        assert call.request.headers["Idempotency-Key"] == "same-key"
        assert json.loads(call.request.content) == {
            "action": "render",
            **PROJECT,
            "title": "Mix",
            "async": True,
        }
