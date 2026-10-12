"""Maestro task query tools."""

import asyncio
from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import _task_outcome, format_result, format_task_result


def _compact_task(data: dict, *, include_output: bool = False) -> dict:
    """Keep task discovery below the agent's tool-result budget.

    The API's list response includes complete briefs and progress logs. Four
    ordinary tasks can exceed the 20,000-character agent result ceiling and
    hide later candidates. Callers can still request the full task explicitly.
    """
    request = data.get("request") or {}
    response = data.get("response") or {}
    variants = (response.get("data") or {}).get("variants") or []
    first_variant = variants[0] if variants and isinstance(variants[0], dict) else {}
    summary = {
        "id": data.get("id"),
        "status": data.get("status"),
        "created_at": data.get("created_at"),
        "finished_at": data.get("finished_at"),
        "duration": request.get("duration"),
        "aspect": request.get("aspect"),
    }
    if include_output:
        progress = data.get("progress") or {}
        summary.update(
            output_url=first_variant.get("output_url"),
            error=str(response.get("error"))[:300] if response.get("error") else None,
            progress={
                "percent": progress.get("percent"),
                "stage": progress.get("stage"),
                "message": str(progress.get("message"))[:200] if progress.get("message") else None,
            },
        )
    return summary


@mcp.tool()
async def maestro_get_task(
    task_id: Annotated[
        str,
        Field(description="Task ID returned by maestro_create_video."),
    ],
    compact: Annotated[
        bool,
        Field(
            description="Return a bounded status and output summary without the full brief or progress log."
        ),
    ] = False,
) -> str:
    """Get live progress and final outputs for one Maestro video task."""
    data = await client.get_task(task_id)
    # Throttle polling: sleep 5s while the task is still running so LLM clients
    # don't burn through poll attempts in seconds.
    is_in_flight, _, _ = _task_outcome(data)
    if is_in_flight:
        await asyncio.sleep(5)
    return format_task_result(_compact_task(data, include_output=True) if compact else data)


@mcp.tool()
async def maestro_list_tasks(
    limit: Annotated[
        int,
        Field(description="Maximum number of recent tasks to return.", ge=1, le=100),
    ] = 20,
    created_at_min: Annotated[
        int | None,
        Field(description="Only include tasks created strictly after this Unix timestamp."),
    ] = None,
    created_at_max: Annotated[
        int | None,
        Field(description="Only include tasks created strictly before this Unix timestamp."),
    ] = None,
    compact: Annotated[
        bool,
        Field(
            description="Return bounded task summaries instead of complete briefs and progress logs."
        ),
    ] = False,
) -> str:
    """List recent Maestro tasks owned by the authenticated user."""
    data = await client.list_tasks(limit, created_at_min, created_at_max)
    if compact:
        data = {**data, "items": [_compact_task(item) for item in data.get("items", [])]}
    return format_result(data)
