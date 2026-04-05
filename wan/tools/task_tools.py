"""Task query tools for Wan API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_batch_task_result, format_task_result


@mcp.tool()
async def wan_get_task(
    task_id: Annotated[
        str,
        Field(
            description="The task ID returned from a generation request. This is the 'task_id' field from any wan_generate_* tool response."
        ),
    ],
) -> str:
    """Query the status and result of a video generation task.

    Use this to check if a generation is complete and retrieve the resulting
    video URLs and metadata.

    Task states:
    - 'pending': Generation is queued
    - 'processing': Generation is in progress
    - 'completed': Generation finished successfully
    - 'failed': Generation failed (check error message)

    Returns:
        Task status and generated video information including URLs.
    """
    result = await client.query_task(
        id=task_id,
        action="retrieve",
    )
    return format_task_result(result)


@mcp.tool()
async def wan_get_tasks_batch(
    task_ids: Annotated[
        list[str],
        Field(description="List of task IDs to query. Maximum recommended batch size is 50 tasks."),
    ],
) -> str:
    """Query multiple video generation tasks at once.

    Efficiently check the status of multiple tasks in a single request.

    Returns:
        Status and video information for all queried tasks.
    """
    result = await client.query_task(
        ids=task_ids,
        action="retrieve_batch",
    )
    return format_batch_task_result(result)
