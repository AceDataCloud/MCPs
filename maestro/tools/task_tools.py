"""Maestro task query tools."""

import asyncio
from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import IN_FLIGHT_STATES, format_task_result


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
    if str(data.get("status", "")).lower() in IN_FLIGHT_STATES:
        await asyncio.sleep(5)
    return format_task_result(data)
