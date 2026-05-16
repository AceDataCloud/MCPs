"""Tasks API tools for OpenAI."""

import json
from typing import Annotated, Any, Literal

from pydantic import Field

from core.client import client
from core.exceptions import OpenAIAPIError, OpenAIAuthError
from core.server import mcp


@mcp.tool()
async def openai_get_task(
    id: Annotated[
        str | None,
        Field(
            description=(
                "Task ID returned by the original image request (e.g. from "
                "openai_generate_image or openai_edit_image when callback_url was set). "
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

    Image generation and editing requests submitted with a callback_url are
    processed asynchronously and produce a persistent task record. Use this
    tool to check whether the task has finished and to retrieve the final
    result.

    Note: tasks are only created when the original request included a
    callback_url. Synchronous (non-callback) calls are not stored.

    Use this when:
    - You previously called openai_generate_image or openai_edit_image with a
      callback_url and want to retrieve the result
    - You want to check the status of an async image task

    Returns:
        JSON object with task details (id, trace_id, type, request, response,
        created_at, finished_at, duration) or an empty object if not found.
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

        if not result:
            return json.dumps({"error": "No response received."})

        return json.dumps(result, ensure_ascii=False, indent=2)

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
                "Filter by upstream type. Options: 'images', "
                "'images_generations', 'images_edits'."
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

    Note: tasks are only created when the original request included a
    callback_url. Synchronous (non-callback) calls are not stored.

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
