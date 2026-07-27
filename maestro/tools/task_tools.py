"""Maestro task query tools."""

import asyncio
from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_result

# States that mean "still working". Anything else (succeeded, failed, dead, or
# a status we don't know yet) returns immediately — an unknown state must not
# strand the caller in a sleep loop.
_IN_FLIGHT_STATES = {"queued", "pending", "planning", "producing", "running", "processing"}


@mcp.tool()
async def maestro_get_task(
    task_id: Annotated[
        str,
        Field(description="Task ID returned by maestro_create_video."),
    ],
) -> str:
    """Get live progress and final outputs for one Maestro video task."""
    data = await client.get_task(task_id)
    # Throttle polling: sleep 5s while the task is still running so LLM clients
    # don't burn through poll attempts in seconds.
    if str(data.get("status", "")).lower() in _IN_FLIGHT_STATES:
        await asyncio.sleep(5)
    return format_result(data)


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
