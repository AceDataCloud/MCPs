"""Maestro task query tools."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_result


@mcp.tool()
async def maestro_get_task(
    task_id: Annotated[
        str,
        Field(description="Task ID returned by maestro_create_video."),
    ],
) -> str:
    """Get live progress and final outputs for one Maestro video task."""
    return format_result(await client.get_task(task_id))


@mcp.tool()
async def maestro_list_tasks(
    limit: Annotated[
        int,
        Field(description="Maximum number of recent tasks to return.", ge=1, le=100),
    ] = 20,
    created_at_min: Annotated[
        int | None,
        Field(description="Optional inclusive lower Unix timestamp for task creation time."),
    ] = None,
    created_at_max: Annotated[
        int | None,
        Field(description="Optional inclusive upper Unix timestamp for task creation time."),
    ] = None,
) -> str:
    """List recent Maestro tasks owned by the authenticated user."""
    return format_result(await client.list_tasks(limit, created_at_min, created_at_max))
