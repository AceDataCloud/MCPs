"""Maestro video creation tools."""

from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import (
    MaestroAction,
    MaestroAspect,
    MaestroQuality,
    MaestroScenario,
    MaestroVoice,
)
from core.utils import format_result


@mcp.tool()
async def maestro_create_video(
    prompt: Annotated[
        str,
        Field(
            description=(
                "Natural-language production brief: topic, audience, scenes, tone, and desired "
                "outcome. Maestro plans the script, assets, voiceover, edit, captions, and render."
            ),
            min_length=1,
        ),
    ],
    action: Annotated[
        MaestroAction,
        Field(
            description=(
                "generate creates a new video. remix, edit, and extend iterate on a previous "
                "Maestro task and require ref_task_id."
            )
        ),
    ] = "generate",
    ref_task_id: Annotated[
        str | None,
        Field(description="Previous Maestro task ID for remix, edit, or extend."),
    ] = None,
    file_urls: Annotated[
        list[str] | None,
        Field(description="Reference image, video, or audio URLs for Maestro to use."),
    ] = None,
    langs: Annotated[
        list[str] | None,
        Field(
            description=(
                "Output language codes, such as zh-cn, en, ja, or pt-br. Each language produces "
                "a localized video variant."
            )
        ),
    ] = None,
    aspect: Annotated[
        MaestroAspect | None,
        Field(
            description=(
                "Output aspect ratio: 9:16, 16:9, or 1:1. Omit to use the server default (9:16) "
                "on a new video, or to inherit the source task's ratio when iterating."
            )
        ),
    ] = None,
    duration: Annotated[
        int | None,
        Field(
            description=(
                "Target video duration in seconds, from 1 to 600. Omit to use the server default "
                "(30) on a new video, or to inherit the source task's duration when iterating."
            ),
            ge=1,
            le=600,
        ),
    ] = None,
    quality: Annotated[
        MaestroQuality | None,
        Field(
            description=(
                "Production tier: draft, standard, or premium. Omit to use the server default "
                "(standard) on a new video, or to inherit the source task's tier when iterating."
            )
        ),
    ] = None,
    scenario: Annotated[
        MaestroScenario | None,
        Field(
            description=(
                "Production workflow: auto, narrated, drama, avatar, motion, or slideshow. "
                "Avatar normally needs a portrait in file_urls. Omit to let the server decide."
            )
        ),
    ] = None,
    style: Annotated[
        str | None,
        Field(
            description=(
                "Visual style preset or freeform style hint, such as cinematic, glass, swiss, "
                "editorial, warm, neon, or futuristic. Omit to let the server decide."
            )
        ),
    ] = None,
    voice: Annotated[
        MaestroVoice | str | None,
        Field(
            description=(
                "Narration voice preset, auto, or a 32-hex-character Fish reference ID. "
                "Omit to let the server decide."
            )
        ),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(description="Optional webhook URL called when the task succeeds or fails."),
    ] = None,
) -> str:
    """Create a complete video or iterate on a prior Maestro video.

    The call returns immediately with a task_id. Use maestro_get_task to monitor progress and obtain
    each completed language variant's output_url, captions_url, cover_url, duration, and QC score.
    """
    if action != "generate" and not ref_task_id:
        return f"Error: action={action} requires ref_task_id."

    # Only send fields the caller set. Omitting them lets the server apply its
    # documented default on a fresh generate and inherit the source task's
    # format (ratio/duration/quality) when iterating, avoiding wrong output and
    # mis-billing on remix/edit/extend.
    payload: dict[str, Any] = {"prompt": prompt, "action": action}
    if ref_task_id:
        payload["ref_task_id"] = ref_task_id
    if aspect is not None:
        payload["aspect"] = aspect
    if duration is not None:
        payload["duration"] = duration
    if quality is not None:
        payload["quality"] = quality
    if scenario is not None:
        payload["scenario"] = scenario
    if style is not None:
        payload["style"] = style
    if voice is not None:
        payload["voice"] = voice
    if file_urls:
        payload["file_urls"] = file_urls
    if langs:
        payload["langs"] = langs
    if callback_url:
        payload["callback_url"] = callback_url

    return format_result(await client.create_video(payload))
