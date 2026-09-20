import json
from unittest.mock import AsyncMock, patch

import pytest

from core.server import mcp
from tools.project_tools import (
    suno_add_project_track,
    suno_commit_project_candidate,
    suno_create_project,
    suno_generate_project_track,
    suno_get_project,
    suno_remove_project_track,
    suno_render_project,
    suno_replace_project_section,
    suno_save_project,
    suno_upload_project_audio,
)


@pytest.mark.asyncio
async def test_create_and_retrieve_use_unified_endpoint_contract():
    with patch(
        "tools.project_tools.client.projects", new=AsyncMock(return_value={"success": True})
    ) as request:
        await suno_create_project(title="Studio", idempotency_key="create-1")
        request.assert_awaited_once_with(
            action="create", title="Studio", idempotency_key="create-1"
        )
    with patch(
        "tools.project_tools.client.projects", new=AsyncMock(return_value={"success": True})
    ) as request:
        await suno_get_project(project_id="project-1")
        request.assert_awaited_once_with(action="retrieve", id="project-1")


@pytest.mark.asyncio
async def test_save_round_trips_complete_state():
    state = {"tracks": [{"id": "track-1", "future": {"keep": True}}], "unknown": [1, 2]}
    with patch(
        "tools.project_tools.client.projects", new=AsyncMock(return_value={"success": True})
    ) as request:
        await suno_save_project("project-1", "v1", state, "save-1", title="Edited")
    assert request.await_args.kwargs == {
        "idempotency_key": "save-1",
        "action": "save",
        "id": "project-1",
        "version_id": "v1",
        "state": state,
        "title": "Edited",
    }


@pytest.mark.asyncio
async def test_async_upload_returns_task_polling_guidance():
    with patch(
        "tools.project_tools.client.projects",
        new=AsyncMock(return_value={"task_id": "task-1", "trace_id": "trace-1"}),
    ):
        result = json.loads(
            await suno_upload_project_audio(
                "project-1", "v1", "https://example.com/audio.mp3", "upload-1"
            )
        )
    assert result["mcp_async_submission"]["poll_tool"] == "suno_get_task"
    assert result["mcp_async_submission"]["task_id"] == "task-1"


@pytest.mark.asyncio
async def test_track_actions_forward_exact_payloads():
    with patch(
        "tools.project_tools.client.projects", new=AsyncMock(return_value={"task_id": "task"})
    ) as request:
        await suno_add_project_track("p", "v", "a", "add", name="Track", gain=0.8)
        assert request.await_args.kwargs == {
            "idempotency_key": "add",
            "action": "add_track",
            "id": "p",
            "version_id": "v",
            "audio_id": "a",
            "name": "Track",
            "gain": 0.8,
        }
    with patch(
        "tools.project_tools.client.projects", new=AsyncMock(return_value={"task_id": "task"})
    ) as request:
        await suno_generate_project_track(
            "p", "v", "source", "render", "add Strings", "chirp-crow", 10, 20, "gen"
        )
        assert request.await_args.kwargs["action"] == "generate_track"
        assert request.await_args.kwargs["id"] == "p"
    with patch(
        "tools.project_tools.client.projects", new=AsyncMock(return_value={"task_id": "task"})
    ) as request:
        await suno_replace_project_section(
            "p", "v", "source", "chirp-carp", 10, 20, "replace", fixed=True
        )
        assert request.await_args.kwargs["action"] == "replace_section"
    with patch(
        "tools.project_tools.client.projects", new=AsyncMock(return_value={"task_id": "task"})
    ) as request:
        await suno_commit_project_candidate("p", "v", "op", "candidate", "track", "commit")
        assert request.await_args.kwargs["candidate_id"] == "candidate"
    with patch(
        "tools.project_tools.client.projects", new=AsyncMock(return_value={"success": True})
    ) as request:
        await suno_remove_project_track("p", "v", "track", "remove")
        assert request.await_args.kwargs["action"] == "remove_track"
    with patch(
        "tools.project_tools.client.projects", new=AsyncMock(return_value={"task_id": "task"})
    ) as request:
        await suno_render_project("p", "v", "Final", "render-key")
        assert request.await_args.kwargs["action"] == "render"


@pytest.mark.asyncio
async def test_project_id_is_exposed_as_id_in_fastmcp_schema():
    tools = {tool.name: tool for tool in await mcp.list_tools()}
    for name in ["suno_get_project", "suno_save_project", "suno_render_project"]:
        assert "id" in tools[name].inputSchema["properties"]
        assert "project_id" not in tools[name].inputSchema["properties"]
    with patch(
        "tools.project_tools.client.projects", new=AsyncMock(return_value={"success": True})
    ) as request:
        await mcp.call_tool("suno_get_project", {"id": "project-1"})
        request.assert_awaited_once_with(action="retrieve", id="project-1")


@pytest.mark.asyncio
async def test_invalid_ranges_are_rejected_before_api_call():
    with pytest.raises(ValueError, match="less than"):
        await suno_generate_project_track(
            "p", "v", "s", "r", "add Bass", "chirp-crow", 20, 10, "key"
        )
    with pytest.raises(ValueError, match="shorter than 26"):
        await suno_replace_project_section("p", "v", "s", "chirp-carp", 0, 26, "key", fixed=True)
