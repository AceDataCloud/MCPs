"""Tool payload tests for Maestro MCP."""

import json
from unittest.mock import AsyncMock, patch

from tools.task_tools import maestro_get_task, maestro_list_tasks
from tools.video_tools import maestro_create_video


async def test_create_video_builds_complete_payload() -> None:
    with patch("tools.video_tools.client.create_video", new_callable=AsyncMock) as create:
        create.return_value = {"success": True, "task_id": "task-1"}
        result = await maestro_create_video(
            prompt="Launch video for a new camera",
            action="generate",
            file_urls=["https://example.com/camera.jpg"],
            langs=["en", "pt-br"],
            aspect="16:9",
            duration=45,
            quality="premium",
            scenario="narrated",
            style="editorial",
            voice="documentary-male",
        )

    create.assert_awaited_once_with(
        {
            "prompt": "Launch video for a new camera",
            "action": "generate",
            "file_urls": ["https://example.com/camera.jpg"],
            "langs": ["en", "pt-br"],
            "aspect": "16:9",
            "duration": 45,
            "quality": "premium",
            "scenario": "narrated",
            "style": "editorial",
            "voice": "documentary-male",
        }
    )
    assert json.loads(result)["task_id"] == "task-1"


async def test_iteration_requires_reference_task() -> None:
    result = await maestro_create_video(prompt="Make it faster", action="remix")

    assert result == "Error: action=remix requires ref_task_id."


async def test_generate_omits_unset_optional_fields() -> None:
    with patch("tools.video_tools.client.create_video", new_callable=AsyncMock) as create:
        create.return_value = {"success": True, "task_id": "task-1"}
        await maestro_create_video(prompt="A quick explainer")

    create.assert_awaited_once_with({"prompt": "A quick explainer", "action": "generate"})


async def test_iteration_does_not_clobber_source_format() -> None:
    with patch("tools.video_tools.client.create_video", new_callable=AsyncMock) as create:
        create.return_value = {"success": True, "task_id": "task-2"}
        await maestro_create_video(
            prompt="Tighten the intro",
            action="edit",
            ref_task_id="task-1",
        )

    create.assert_awaited_once_with(
        {"prompt": "Tighten the intro", "action": "edit", "ref_task_id": "task-1"}
    )


async def test_task_tools_delegate_to_client() -> None:
    with (
        patch("tools.task_tools.client.get_task", new_callable=AsyncMock) as get_task,
        patch("tools.task_tools.client.list_tasks", new_callable=AsyncMock) as list_tasks,
    ):
        get_task.return_value = {"id": "task-1", "status": "succeeded"}
        list_tasks.return_value = {"count": 1, "items": []}

        await maestro_get_task("task-1")
        await maestro_list_tasks(5, 100, 200)

    get_task.assert_awaited_once_with("task-1")
    list_tasks.assert_awaited_once_with(5, 100, 200)
