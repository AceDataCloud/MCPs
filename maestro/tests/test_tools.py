"""Tool payload tests for Maestro MCP."""

import json
from unittest.mock import AsyncMock, patch

from core.types import MaestroAsset, MaestroBrand
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
            scenario="captions",
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
            "scenario": "captions",
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


async def test_launch_product_inputs_reach_the_api_without_extra_voice() -> None:
    with patch("tools.video_tools.client.create_video", new_callable=AsyncMock) as create:
        create.return_value = {"success": True, "task_id": "task-1"}
        await maestro_create_video(
            prompt="Launch",
            style="apple-launch",
            audio_mode="music",
            assets=[
                MaestroAsset(id="hero", role="ui_screenshot", url="https://example.com/ui.png")
            ],
            brand=MaestroBrand(name="Acme"),
            website_url="https://example.com",
        )
    payload = create.call_args.args[0]
    assert payload["assets"] == [
        {"id": "hero", "role": "ui_screenshot", "url": "https://example.com/ui.png"}
    ]
    assert payload["brand"] == {"name": "Acme"}
    assert payload["audio_mode"] == "music" and "voice" not in payload


async def test_iteration_explicit_clear_survives_mcp_context() -> None:
    from types import SimpleNamespace

    context = SimpleNamespace(
        request_context=SimpleNamespace(
            request=SimpleNamespace(
                params=SimpleNamespace(arguments={"brand": None, "website_url": None})
            )
        )
    )
    with (
        patch("tools.video_tools.mcp.get_context", return_value=context),
        patch("tools.video_tools.client.create_video", new_callable=AsyncMock) as create,
    ):
        create.return_value = {"success": True, "task_id": "task-1"}
        await maestro_create_video(
            prompt="Clear", action="edit", ref_task_id="source", assets=[], file_urls=[]
        )
    payload = create.call_args.args[0]
    assert payload["brand"] is None and payload["website_url"] is None
    assert payload["assets"] == [] and payload["file_urls"] == []


async def test_iteration_does_not_clobber_source_format() -> None:
    with patch("tools.video_tools.client.create_video", new_callable=AsyncMock) as create:
        create.return_value = {"success": True, "task_id": "task-2"}
        await maestro_create_video(
            prompt="Tighten the intro",
            action="edit",
            ref_task_id="task-1",
        )

    create.assert_awaited_once_with(
        {
            "prompt": "Tighten the intro",
            "action": "edit",
            "ref_task_id": "task-1",
        }
    )


async def test_all_documented_actions_are_accepted() -> None:
    with patch("tools.video_tools.client.create_video", new_callable=AsyncMock) as create:
        create.return_value = {"success": True, "task_id": "task-1"}
        await maestro_create_video(
            prompt="x", action="extend", ref_task_id="task-1", duration=300, scenario="drama"
        )

    create.assert_awaited_once_with(
        {
            "prompt": "x",
            "action": "extend",
            "ref_task_id": "task-1",
            "duration": 300,
            "scenario": "drama",
        }
    )


async def test_task_tools_delegate_to_client() -> None:
    with patch("tools.task_tools.client.get_task", new_callable=AsyncMock) as get_task:
        get_task.return_value = {"id": "task-1", "finished_at": 1, "response": {}}

        await maestro_get_task("task-1")

    get_task.assert_awaited_once_with("task-1")


async def test_list_tasks_delegates_filters_to_client() -> None:
    with patch("tools.task_tools.client.list_tasks", new_callable=AsyncMock) as list_tasks:
        list_tasks.return_value = {"count": 0, "items": []}

        result = await maestro_list_tasks(30, 100, 200)

    list_tasks.assert_awaited_once_with(30, 100, 200)
    assert json.loads(result) == {"count": 0, "items": []}


async def test_list_tasks_uses_public_defaults() -> None:
    with patch("tools.task_tools.client.list_tasks", new_callable=AsyncMock) as list_tasks:
        list_tasks.return_value = {"count": 0, "items": []}

        await maestro_list_tasks()

    list_tasks.assert_awaited_once_with(20, None, None)
