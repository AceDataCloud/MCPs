"""Suno Studio project workflow tools."""

import json
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_audio_result


def _payload(**values: Any) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


def _format(result: dict[str, Any]) -> str:
    if "task_id" in result and not result.get("data"):
        return format_audio_result(result)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def suno_create_project(
    title: Annotated[str, Field(min_length=1, max_length=200, description="Project title.")],
    idempotency_key: Annotated[
        str, Field(min_length=1, max_length=128, description="Unique retry key.")
    ],
) -> str:
    """Create an empty Studio project."""
    return _format(
        await client.projects(action="create", title=title, idempotency_key=idempotency_key)
    )


@mcp.tool()
async def suno_get_project(
    project_id: Annotated[str, Field(description="Project ID.", validation_alias="id")],
) -> str:
    """Retrieve the current project version and complete editable state."""
    return _format(await client.projects(action="retrieve", id=project_id))


@mcp.tool()
async def suno_save_project(
    project_id: Annotated[str, Field(description="Project ID.", validation_alias="id")],
    version_id: Annotated[str, Field(description="Current project version from retrieve.")],
    state: Annotated[
        dict[str, Any], Field(description="Complete project state from retrieve, including edits.")
    ],
    idempotency_key: Annotated[
        str, Field(min_length=1, max_length=128, description="Unique retry key.")
    ],
    title: Annotated[str | None, Field(description="Optional updated title.")] = None,
) -> str:
    """Save a complete Studio project state using optimistic concurrency."""
    return _format(
        await client.projects(
            idempotency_key=idempotency_key,
            **_payload(
                action="save", id=project_id, version_id=version_id, state=state, title=title
            ),
        )
    )


@mcp.tool()
async def suno_upload_project_audio(
    project_id: Annotated[str, Field(description="Project ID.", validation_alias="id")],
    version_id: Annotated[str, Field(description="Current project version.")],
    audio_url: Annotated[str, Field(pattern=r"^https://", description="Public HTTPS audio URL.")],
    idempotency_key: Annotated[
        str, Field(min_length=1, max_length=128, description="Unique retry key.")
    ],
    callback_url: Annotated[
        str | None, Field(description="Optional HTTPS completion webhook.")
    ] = None,
) -> str:
    """Upload an authorized audio URL and initialize a Studio-ready clip."""
    return _format(
        await client.projects(
            idempotency_key=idempotency_key,
            **_payload(
                action="upload",
                id=project_id,
                version_id=version_id,
                audio_url=audio_url,
                callback_url=callback_url,
            ),
        )
    )


@mcp.tool()
async def suno_add_project_track(
    project_id: Annotated[str, Field(description="Project ID.", validation_alias="id")],
    version_id: Annotated[str, Field(description="Current project version.")],
    audio_id: Annotated[str, Field(description="Existing Suno audio ID.")],
    idempotency_key: Annotated[
        str, Field(min_length=1, max_length=128, description="Unique retry key.")
    ],
    name: Annotated[str | None, Field(description="Optional track name.")] = None,
    start_beats: Annotated[
        float | None, Field(description="Optional placement start in beats.")
    ] = None,
    end_beats: Annotated[
        float | None, Field(description="Optional placement end in beats.")
    ] = None,
    gain: Annotated[float | None, Field(ge=0, description="Optional track gain.")] = None,
) -> str:
    """Add an existing audio clip as a new project track."""
    return _format(
        await client.projects(
            idempotency_key=idempotency_key,
            **_payload(
                action="add_track",
                id=project_id,
                version_id=version_id,
                audio_id=audio_id,
                name=name,
                start_beats=start_beats,
                end_beats=end_beats,
                gain=gain,
            ),
        )
    )


@mcp.tool()
async def suno_generate_project_track(
    project_id: Annotated[str, Field(description="Project ID.", validation_alias="id")],
    version_id: Annotated[str, Field(description="Current project version.")],
    source_audio_id: Annotated[
        str, Field(description="Source audio used to preserve surrounding context.")
    ],
    render_audio_id: Annotated[
        str, Field(description="Rendered project audio used for conditioning.")
    ],
    stem_control_tags: Annotated[
        str, Field(description="Track instruction such as add Strings or add Drums.")
    ],
    model: Annotated[str, Field(description="Suno model identifier.")],
    start_seconds: Annotated[float, Field(ge=0, description="Generation range start in seconds.")],
    end_seconds: Annotated[float, Field(gt=0, description="Generation range end in seconds.")],
    idempotency_key: Annotated[
        str, Field(min_length=1, max_length=128, description="Unique retry key.")
    ],
    title: str | None = None,
    tags: str | None = None,
    prompt: str | None = None,
) -> str:
    """Generate new track candidates without silently committing one."""
    if start_seconds >= end_seconds:
        raise ValueError("start_seconds must be less than end_seconds")
    return _format(
        await client.projects(
            idempotency_key=idempotency_key,
            **_payload(
                action="generate_track",
                id=project_id,
                version_id=version_id,
                source_audio_id=source_audio_id,
                render_audio_id=render_audio_id,
                stem_control_tags=stem_control_tags,
                model=model,
                start_seconds=start_seconds,
                end_seconds=end_seconds,
                title=title,
                tags=tags,
                prompt=prompt,
            ),
        )
    )


@mcp.tool()
async def suno_replace_project_section(
    project_id: Annotated[str, Field(description="Project ID.", validation_alias="id")],
    version_id: Annotated[str, Field(description="Current project version.")],
    source_audio_id: Annotated[str, Field(description="Audio containing the section to replace.")],
    model: Annotated[str, Field(description="Suno model identifier.")],
    start_seconds: Annotated[float, Field(ge=0)],
    end_seconds: Annotated[float, Field(gt=0)],
    idempotency_key: Annotated[str, Field(min_length=1, max_length=128)],
    replacement_lyrics: str | None = None,
    prompt: str | None = None,
    tags: str | None = None,
    fixed: bool = False,
) -> str:
    """Generate two replacement candidates for a project section."""
    if start_seconds >= end_seconds:
        raise ValueError("start_seconds must be less than end_seconds")
    if fixed and end_seconds - start_seconds >= 26:
        raise ValueError("fixed replacement must be shorter than 26 seconds")
    return _format(
        await client.projects(
            idempotency_key=idempotency_key,
            **_payload(
                action="replace_section",
                id=project_id,
                version_id=version_id,
                source_audio_id=source_audio_id,
                model=model,
                start_seconds=start_seconds,
                end_seconds=end_seconds,
                replacement_lyrics=replacement_lyrics,
                prompt=prompt,
                tags=tags,
                fixed=fixed,
            ),
        )
    )


@mcp.tool()
async def suno_commit_project_candidate(
    project_id: Annotated[str, Field(description="Project ID.", validation_alias="id")],
    version_id: Annotated[str, Field(description="Version on which candidates were generated.")],
    operation_id: Annotated[str, Field(description="Candidate generation task/operation ID.")],
    candidate_id: Annotated[str, Field(description="Chosen candidate ID.")],
    track_id: Annotated[str, Field(description="Track receiving the candidate.")],
    idempotency_key: Annotated[str, Field(min_length=1, max_length=128)],
    start_beats: float | None = None,
    end_beats: float | None = None,
) -> str:
    """Commit one generated candidate to the current project version."""
    return _format(
        await client.projects(
            idempotency_key=idempotency_key,
            **_payload(
                action="commit_candidate",
                id=project_id,
                version_id=version_id,
                operation_id=operation_id,
                candidate_id=candidate_id,
                track_id=track_id,
                start_beats=start_beats,
                end_beats=end_beats,
            ),
        )
    )


@mcp.tool()
async def suno_remove_project_track(
    project_id: Annotated[str, Field(description="Project ID.", validation_alias="id")],
    version_id: Annotated[str, Field(description="Current project version.")],
    track_id: Annotated[str, Field(description="Track ID to remove.")],
    idempotency_key: Annotated[str, Field(min_length=1, max_length=128)],
) -> str:
    """Remove a track and save a new project version."""
    return _format(
        await client.projects(
            action="remove_track",
            id=project_id,
            version_id=version_id,
            track_id=track_id,
            idempotency_key=idempotency_key,
        )
    )


@mcp.tool()
async def suno_render_project(
    project_id: Annotated[str, Field(description="Project ID.", validation_alias="id")],
    version_id: Annotated[str, Field(description="Saved project version to render.")],
    title: Annotated[str, Field(min_length=1, description="Export title.")],
    idempotency_key: Annotated[str, Field(min_length=1, max_length=128)],
    lyrics: str | None = None,
    tags: str | None = None,
    start_beats: float | None = None,
    end_beats: float | None = None,
    callback_url: str | None = None,
) -> str:
    """Render an authoritative saved project version into a final song."""
    return _format(
        await client.projects(
            idempotency_key=idempotency_key,
            **_payload(
                action="render",
                id=project_id,
                version_id=version_id,
                title=title,
                lyrics=lyrics,
                tags=tags,
                start_beats=start_beats,
                end_beats=end_beats,
                callback_url=callback_url,
            ),
        )
    )
