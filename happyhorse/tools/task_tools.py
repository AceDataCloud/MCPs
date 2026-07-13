"""Task query tools for Happy Horse."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_batch_task_result, format_task_result


@mcp.tool()
async def happyhorse_get_task(
    task_id: Annotated[
        str,
        Field(description="Task ID returned by a Happy Horse generation or edit tool."),
    ],
) -> str:
    """Get the status and final video URL for one Happy Horse task."""
    return format_task_result(await client.get_task(task_id))


@mcp.tool()
async def happyhorse_get_tasks_batch(
    task_ids: Annotated[
        list[str],
        Field(description="One to fifty Happy Horse task IDs.", min_length=1, max_length=50),
    ],
) -> str:
    """Get multiple Happy Horse tasks in one request."""
    if not 1 <= len(task_ids) <= 50:
        return "Error: task_ids must contain between 1 and 50 IDs."
    return format_batch_task_result(await client.get_tasks_batch(task_ids))
