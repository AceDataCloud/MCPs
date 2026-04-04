"""Task query tools for Luma API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_batch_task_result, format_task_result


@mcp.tool()
async def luma_get_task(
    task_id: Annotated[
        str,
        Field(
            description="The task ID returned from a generation request. This is the 'task_id' field from any luma_generate_* or luma_extend_* tool response."
        ),
    ],
) -> str:
    """Query the status and result of a video generation task.

    Use this to check if a generation is complete and retrieve the resulting
    video URLs, thumbnails, and other metadata.

    Use this when:
    - You want to check if a generation has completed
    - You need to retrieve video URLs from a previous generation
    - You want to get the full details of a generated video

    Task states:
    - 'pending': Generation is still in progress
    - 'completed': Generation finished successfully
    - 'failed': Generation failed (check error message)

    Returns:
        Task status and generated video information including URLs, dimensions, and thumbnail.
    """
    result = await client.query_task(
        id=task_id,
        action="retrieve",
    )
    return format_task_result(result)


@mcp.tool()
async def luma_get_tasks_batch(
    task_ids: Annotated[
        list[str],
        Field(description="List of task IDs to query. Maximum recommended batch size is 50 tasks."),
    ],
) -> str:
    """Query multiple video generation tasks at once.

    Efficiently check the status of multiple tasks in a single request.
    More efficient than calling luma_get_task multiple times.

    Use this when:
    - You have multiple pending generations to check
    - You want to get status of several videos at once
    - You're tracking a batch of generations

    Returns:
        Status and video information for all queried tasks.
    """
    result = await client.query_task(
        ids=task_ids,
        action="retrieve_batch",
    )
    return format_batch_task_result(result)
