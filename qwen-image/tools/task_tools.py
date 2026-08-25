"""Task query tools for Qwen Image API."""

import asyncio
from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_batch_task_result, format_task_result


@mcp.tool()
async def qwen_image_get_task(
    task_id: Annotated[
        str,
        Field(
            description="The task ID returned from a generation or edit request. "
            "This is the 'task_id' field from any qwen_image_generate or "
            "qwen_image_edit tool response."
        ),
    ],
) -> str:
    """Query the status and result of a Qwen Image image generation or edit task.

    Use this to check if a generation/edit is complete and retrieve the resulting
    image URLs and metadata.

    Use this when:
    - You want to check if an image generation has completed
    - You need to retrieve image URLs from a previous generation
    - You want to get the full details of a generated/edited image

    Returns:
        Task status and image information including URLs, prompts, and metadata.
    """
    result = await client.query_task(
        id=task_id,
        action="retrieve",
    )
    # Throttle polling: sleep 5s for incomplete tasks so LLM clients
    # don't burn through poll attempts in seconds.
    response = result.get("response", {})
    is_complete = response.get("success") is True
    is_failed = response.get("success") is False or str(result.get("state", "")).lower() in {
        "failed",
        "error",
        "cancelled",
        "canceled",
    }
    if not is_complete and not is_failed:
        await asyncio.sleep(5)
    return format_task_result(result)


@mcp.tool()
async def qwen_image_get_tasks_batch(
    task_ids: Annotated[
        list[str],
        Field(description="List of task IDs to query. Allows querying multiple tasks at once."),
    ],
) -> str:
    """Query multiple Qwen Image image tasks at once.

    Efficiently check the status of multiple tasks in a single request.
    More efficient than calling qwen_image_get_task multiple times.

    Use this when:
    - You have multiple pending generations to check
    - You want to get status of several images at once
    - You're tracking a batch of generations

    Returns:
        Status and image information for all queried tasks.
    """
    result = await client.query_task(
        ids=task_ids,
        action="retrieve_batch",
    )
    return format_batch_task_result(result)
