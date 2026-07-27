"""Task query tools for Happy Horse."""

import asyncio
from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_batch_task_result, format_task_result, is_task_settled


@mcp.tool()
async def happyhorse_get_task(
    task_id: Annotated[
        str,
        Field(description="Task ID returned by a Happy Horse generation or edit tool."),
    ],
) -> str:
    """Get the status and final video URL for one Happy Horse task."""
    data = await client.get_task(task_id)
    # Throttle polling: sleep 5s while the task is still running so LLM clients
    # don't burn through poll attempts in seconds. Terminal states return now.
    if not is_task_settled(data):
        await asyncio.sleep(5)
    return format_task_result(data)


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
