"""Task query tools for Fish API."""

import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import FishAPIError, FishAuthError
from core.server import mcp


@mcp.tool()
async def fish_get_task(
    task_id: Annotated[
        str,
        Field(
            description=(
                "The task ID returned from a fish_generate_audio or fish_create_voice request. "
                "This is the 'task_id' field in the response."
            )
        ),
    ],
) -> str:
    """Query the status and result of a Fish audio generation or voice cloning task.

    Use this to check if a task is complete and retrieve the resulting audio URL
    or voice ID.

    Task states:
    - 'pending': Task is queued — keep polling
    - 'processing': Task is being processed — keep polling
    - 'complete': Task finished successfully
    - 'failed': Task failed (check error message)

    Returns:
        Task status and result data including audio URL or voice ID.
    """
    if not task_id:
        return json.dumps({"error": "Validation Error", "message": "task_id is required"})

    try:
        result = await client.query_task(id=task_id, action="retrieve")

        if not result:
            return json.dumps({"error": "No response received from the API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except FishAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except FishAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error querying task", "message": str(e)})


@mcp.tool()
async def fish_get_tasks_batch(
    task_ids: Annotated[
        list[str],
        Field(description="List of task IDs to query status for."),
    ],
) -> str:
    """Query the status of multiple Fish tasks at once.

    Efficiently checks the status of multiple audio generation or voice cloning
    tasks in a single request.

    Returns:
        Status and result data for all queried tasks.
    """
    if not task_ids:
        return json.dumps({"error": "Validation Error", "message": "task_ids is required"})

    try:
        result = await client.query_task(ids=task_ids, action="retrieve_batch")

        if not result:
            return json.dumps({"error": "No response received from the API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except FishAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except FishAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error querying tasks", "message": str(e)})
