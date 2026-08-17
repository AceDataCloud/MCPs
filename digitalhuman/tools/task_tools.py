"""Task query tools for Digital Human."""

import asyncio
import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import DigitalHumanAPIError, DigitalHumanAuthError
from core.server import mcp
from core.utils import format_batch_task_result, format_task_result, is_task_settled


@mcp.tool()
async def digitalhuman_get_task(
    task_id: Annotated[
        str,
        Field(
            description="Task ID returned by a Digital Human create-video or clone-voice request."
        ),
    ],
    action: Annotated[
        str | None,
        Field(
            description=(
                "Optional action. Omit for the flat poll shape. Use 'retrieve' for the detailed "
                "shape with created_at, started_at, finished_at, and elapsed."
            ),
            pattern="^retrieve$",
        ),
    ] = None,
) -> str:
    """Get the status and final result for one Digital Human task."""
    try:
        data = await client.get_task(task_id, action=action)
        if not is_task_settled(data):
            await asyncio.sleep(5)
        return format_task_result(data)
    except DigitalHumanAuthError as exc:
        return json.dumps({"error": "Authentication Error", "message": exc.message})
    except DigitalHumanAPIError as exc:
        return json.dumps({"error": "API Error", "message": exc.message})
    except Exception as exc:
        return json.dumps({"error": "Error querying task", "message": str(exc)})


@mcp.tool()
async def digitalhuman_get_tasks_batch(
    task_ids: Annotated[
        list[str],
        Field(description="List of Digital Human task IDs to query.", min_length=1),
    ],
) -> str:
    """Get multiple Digital Human tasks in one request."""
    if not task_ids:
        return json.dumps({"error": "Validation Error", "message": "task_ids is required"})
    try:
        return format_batch_task_result(await client.get_tasks_batch(task_ids))
    except DigitalHumanAuthError as exc:
        return json.dumps({"error": "Authentication Error", "message": exc.message})
    except DigitalHumanAPIError as exc:
        return json.dumps({"error": "API Error", "message": exc.message})
    except Exception as exc:
        return json.dumps({"error": "Error querying tasks", "message": str(exc)})


@mcp.tool()
async def digitalhuman_delete_task(
    task_id: Annotated[
        str,
        Field(description="Task ID of the Digital Human task to delete."),
    ],
) -> str:
    """Delete one Digital Human task."""
    if not task_id:
        return json.dumps({"error": "Validation Error", "message": "task_id is required"})
    try:
        return json.dumps(await client.delete_task(task_id), ensure_ascii=False, indent=2)
    except DigitalHumanAuthError as exc:
        return json.dumps({"error": "Authentication Error", "message": exc.message})
    except DigitalHumanAPIError as exc:
        return json.dumps({"error": "API Error", "message": exc.message})
    except Exception as exc:
        return json.dumps({"error": "Error deleting task", "message": str(exc)})
