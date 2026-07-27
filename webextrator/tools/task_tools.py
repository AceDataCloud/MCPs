"""Task query tools for WebExtrator API."""

import asyncio
import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import WebExtraterAPIError, WebExtraterAuthError
from core.server import mcp
from core.utils import _task_outcome, format_task_result


@mcp.tool()
async def webextrator_get_task(
    task_id: Annotated[
        str | None,
        Field(
            description=(
                "Task UUID to retrieve. Use this to get the result of a single "
                "extract or render task."
            )
        ),
    ] = None,
    trace_id: Annotated[
        str | None,
        Field(
            description=(
                "Trace UUID as an alternative lookup for a single task. "
                "Use either task_id or trace_id."
            )
        ),
    ] = None,
) -> str:
    """Retrieve the result of a single previously created extract or render task.

    Use this when:
    - You submitted an extract or render request and got back a task_id
    - You want to poll for the result of a specific task by its ID

    Returns:
        JSON response containing the task status and result data.
    """
    if not task_id and not trace_id:
        return json.dumps(
            {"error": "Validation Error", "message": "Either task_id or trace_id is required"}
        )

    try:
        result = await client.query_tasks(
            action="retrieve",
            id=task_id,
            trace_id=trace_id,
        )

        if not result:
            return json.dumps(
                {
                    "error": "Task not found",
                    "message": "No task matches that task_id or trace_id. Check the id returned by the original request.",
                }
            )

        # Throttle polling: sleep 5s while the task is still running so LLM
        # clients don't burn through poll attempts in seconds. The worker only
        # stamps `finished_at` once the job settles.
        is_complete, is_failed = _task_outcome(result)
        if not (is_complete or is_failed):
            await asyncio.sleep(5)

        return format_task_result(result)

    except WebExtraterAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except WebExtraterAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error retrieving task", "message": str(e)})


@mcp.tool()
async def webextrator_get_tasks_batch(
    ids: Annotated[
        list[str] | None,
        Field(description="List of task UUIDs to retrieve in batch."),
    ] = None,
    trace_ids: Annotated[
        list[str] | None,
        Field(description="List of trace UUIDs to retrieve in batch."),
    ] = None,
    offset: Annotated[
        int | None,
        Field(description="Pagination offset for batch retrieval. Default is 0."),
    ] = None,
    limit: Annotated[
        int | None,
        Field(description="Pagination limit for batch retrieval, 1-100. Default is 50."),
    ] = None,
) -> str:
    """Retrieve the results of multiple previously created extract or render tasks.

    Use this when:
    - You submitted multiple async requests and want to check their results together
    - You want to paginate through a list of tasks

    Returns:
        JSON response containing the list of task statuses and result data.
    """
    if not ids and not trace_ids:
        return json.dumps(
            {"error": "Validation Error", "message": "Either ids or trace_ids is required"}
        )

    try:
        result = await client.query_tasks(
            action="retrieve_batch",
            ids=ids,
            trace_ids=trace_ids,
            offset=offset,
            limit=limit,
        )

        if not result:
            return json.dumps({"error": "No response received from the API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except WebExtraterAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except WebExtraterAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error retrieving tasks batch", "message": str(e)})
