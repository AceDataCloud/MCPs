"""Tasks API tools for OpenAI."""

import asyncio
import json
from typing import Annotated, Any, Literal

from pydantic import Field

from core.client import client
from core.exceptions import OpenAIAPIError, OpenAIAuthError
from core.server import mcp
from core.utils import _task_outcome, format_task_result


def _is_task_finished(result: dict[str, Any]) -> bool:
    """A task is done once the worker has stamped `finished_at` on it.

    Shares `_task_outcome` with the guidance block so the throttle and the
    advertised `should_poll` can never disagree.
    """
    is_complete, is_failed = _task_outcome(result)
    return is_complete or is_failed


@mcp.tool()
async def openai_get_task(
    id: Annotated[
        str | None,
        Field(
            description=(
                "Task ID returned by the original image request (e.g. from "
                "openai_generate_image or openai_edit_image). "
                "At least one of 'id' or 'trace_id' must be provided."
            )
        ),
    ] = None,
    trace_id: Annotated[
        str | None,
        Field(
            description=(
                "Custom trace ID supplied via the 'trace_id' field on the original "
                "image request. When both 'id' and 'trace_id' are given, 'trace_id' "
                "takes precedence."
            )
        ),
    ] = None,
) -> str:
    """Retrieve a single async image task by its task ID or custom trace ID.

    Image generation and editing requests are submitted asynchronously and
    return a task_id immediately. Use this tool to poll until the task
    finishes and to retrieve the final image URLs.

    A task is complete once it carries a `finished_at` timestamp. While it is
    still running this tool waits ~5s before returning, so repeated calls
    poll at a sane rate.

    Use this when:
    - You called openai_generate_image or openai_edit_image and got a task_id
    - You want to check the status of an async image task

    Returns:
        JSON object with task details (id, trace_id, type, request, response,
        created_at, started_at, finished_at, elapsed) or an empty object if not found.
    """
    if id is None and trace_id is None:
        return json.dumps({"error": "At least one of 'id' or 'trace_id' must be provided."})

    try:
        payload: dict[str, Any] = {"action": "retrieve"}
        if id is not None:
            payload["id"] = id
        if trace_id is not None:
            payload["trace_id"] = trace_id

        result = await client.tasks(**payload)

        # The worker answers `{}` for an unknown id — say so plainly instead of
        # reporting it as a transport failure the model would retry forever.
        if not result:
            return json.dumps(
                {
                    "error": "Task not found",
                    "message": "No task matches that id or trace_id. Check the id returned by the original image request.",
                }
            )

        # Throttle polling: sleep 5s while the task is still running so LLM
        # clients don't burn through poll attempts in seconds. The worker only
        # writes `finished_at` once the upstream call returns.
        if not _is_task_finished(result):
            await asyncio.sleep(5)

        return format_task_result(result)

    except OpenAIAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except OpenAIAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error retrieving task", "message": str(e)})


@mcp.tool()
async def openai_list_tasks(
    ids: Annotated[
        list[str] | None,
        Field(description="List of task IDs to retrieve."),
    ] = None,
    trace_ids: Annotated[
        list[str] | None,
        Field(description="List of custom trace IDs to retrieve."),
    ] = None,
    application_id: Annotated[
        str | None,
        Field(description="List all tasks belonging to the specified application."),
    ] = None,
    user_id: Annotated[
        str | None,
        Field(description="List all tasks belonging to the specified end user."),
    ] = None,
    type: Annotated[
        Literal["images", "images_generations", "images_edits"] | None,
        Field(
            description=(
                "Filter by upstream type. Options: 'images', 'images_generations', 'images_edits'."
            )
        ),
    ] = None,
    offset: Annotated[
        int | None,
        Field(description="Pagination offset. Default is 0."),
    ] = None,
    limit: Annotated[
        int | None,
        Field(description="Number of tasks per page. Default is 12."),
    ] = None,
    created_at_min: Annotated[
        float | None,
        Field(description="Earliest task creation timestamp (Unix seconds, inclusive)."),
    ] = None,
    created_at_max: Annotated[
        float | None,
        Field(description="Latest task creation timestamp (Unix seconds, inclusive)."),
    ] = None,
) -> str:
    """List async image tasks using batch query filters.

    Returns a paginated list of async image task records. You must provide at
    least one filter: ids, trace_ids, application_id, user_id, or a
    created_at_min / created_at_max time window.

    Every image generation and edit produces a task record, so this lists
    recent image work regardless of whether a callback_url was used.

    Use this when:
    - You want to list multiple tasks at once
    - You want to see all tasks for an application or user

    Returns:
        JSON object with 'items' array and 'count' field.
    """
    try:
        payload: dict[str, Any] = {"action": "retrieve_batch"}
        if ids is not None:
            payload["ids"] = ids
        if trace_ids is not None:
            payload["trace_ids"] = trace_ids
        if application_id is not None:
            payload["application_id"] = application_id
        if user_id is not None:
            payload["user_id"] = user_id
        if type is not None:
            payload["type"] = type
        if offset is not None:
            payload["offset"] = offset
        if limit is not None:
            payload["limit"] = limit
        if created_at_min is not None:
            payload["created_at_min"] = created_at_min
        if created_at_max is not None:
            payload["created_at_max"] = created_at_max

        result = await client.tasks(**payload)

        if not result:
            return json.dumps({"error": "No response received."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except OpenAIAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except OpenAIAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error listing tasks", "message": str(e)})
