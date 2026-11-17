"""Authenticated free ACE Music task lookup."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_result


@mcp.tool()
async def acemusic_get_task(
    task_id: Annotated[str, Field(min_length=1, description="The original platform task_id.")],
) -> str:
    """Retrieve your existing task and its song-group state without generating.

    Inspect the persisted response and group state. Partial failure is terminal:
    keep any successful audio and report the failed candidate. An audio URL by
    itself does not prove that the entire group has completed.
    """
    return format_result(await client.query_task(action="retrieve", id=task_id))


@mcp.tool()
async def acemusic_get_tasks_batch(
    task_ids: Annotated[list[str], Field(min_length=1, max_length=50)],
) -> str:
    """Retrieve up to 50 original task IDs in one authenticated free request."""
    return format_result(await client.query_task(action="retrieve_batch", ids=task_ids))


@mcp.tool()
async def acemusic_list_tasks(
    page: Annotated[int, Field(ge=1)] = 1,
    page_size: Annotated[int, Field(ge=1, le=50)] = 20,
) -> str:
    """List the caller's ACE Music task history with bounded pagination."""
    return format_result(
        await client.query_task(action="list", limit=page_size, offset=(page - 1) * page_size)
    )
