"""Versioned Suno Studio project operations."""

import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.project_types import SunoProjectRequest
from core.server import mcp
from core.utils import format_audio_result


@mcp.tool()
async def suno_manage_project(
    request: SunoProjectRequest,
    idempotency_key: Annotated[
        str | None,
        Field(
            min_length=1,
            max_length=128,
            description=(
                "Required for every action except retrieve. Choose a new stable key for each "
                "intended write; retry an uncertain submission with the SAME key and identical "
                "request. Changing the key can create a second billable operation."
            ),
        ),
    ] = None,
) -> str:
    """Create, retrieve, save, upload, add/generate/replace tracks, commit, remove, or render a project.

    Use the latest version_id for mutations. Seconds describe the source audio;
    beats describe the project timeline. Generation only creates candidates;
    commit_candidate explicitly adds one to the selected track. Preserve returned
    project/version/operation/candidate IDs. Poll accepted task_id with suno_get_task
    until finished_at is set, then inspect response.success. On timeout, retry the
    SAME request/key or poll its original task; never automatically regenerate.
    """
    if request.action != "retrieve" and not (idempotency_key and idempotency_key.strip()):
        raise ValueError("idempotency_key is required for every project action except retrieve")
    result = await client.manage_project(
        idempotency_key=idempotency_key,
        **request.model_dump(mode="json", by_alias=True, exclude_none=True),
    )
    # Synchronous reads/writes may also include task_id; they are already done.
    if "success" in result:
        return json.dumps(result, ensure_ascii=False, indent=2)
    return format_audio_result(result)
