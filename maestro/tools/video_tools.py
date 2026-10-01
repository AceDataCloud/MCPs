"""Maestro video creation tools."""

from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import (
    MaestroAction,
    MaestroAspect,
    MaestroAsset,
    MaestroAudioMode,
    MaestroBrand,
    MaestroScenario,
    MaestroStyle,
    MaestroVoice,
)
from core.utils import format_submission_result


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
        Field(
            description="Reference image, video, or audio URLs for Maestro to use.",
            max_length=20,
        ),
    ] = None,
    langs: Annotated[
        list[str] | None,
        Field(
            description=(
                "Output language codes, such as zh-cn, en, ja, or pt-br. Each language produces "
                "a localized video variant."
            ),
            max_length=4,
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
                "Target video duration in seconds, from 5 to 300. Omit to use the server default "
                "(30) on a new video, or to inherit the source task's duration when iterating."
            ),
            ge=5,
            le=300,
        ),
    ] = None,
    scenario: Annotated[
        MaestroScenario | None,
        Field(
            description=(
                "Production workflow: auto, narrated, captions, avatar, or drama. Captions "
                "requires a source video in file_urls. Avatar normally needs a portrait in "
                "file_urls. Omit to let the server decide."
            )
        ),
    ] = None,
    style: Annotated[
        MaestroStyle | None,
        Field(
            description=(
                "Visual style preset or custom hint. apple-launch is a restrained product launch "
                "style for auto/narrated; glass is Liquid Glass. Other presets: cinematic, "
                "luxury, swiss, modern, editorial, warm, vibrant, neon, mono, pastel, bold, "
                "industrial, futuristic, retro. Use 'auto' or omit to let the server decide."
            ),
            max_length=40,
        ),
    ] = None,
    voice: Annotated[
        MaestroVoice | None,
        Field(description=("Narration voice preset. Use 'auto' or omit to let the server decide.")),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(description="Optional webhook URL called when the task succeeds or fails."),
    ] = None,
    audio_mode: Annotated[
        MaestroAudioMode | None,
        Field(
            description="auto, narration, music-only, or intentional silent. Omit to inherit when editing; do not pin a voice for music/silent."
        ),
    ] = None,
    assets: Annotated[
        list[MaestroAsset] | None,
        Field(
            description="Role-labeled product/logo/UI/style/music inputs. Combined with file_urls: at most 20. [] clears labeled assets on edit.",
            max_length=20,
        ),
    ] = None,
    brand: Annotated[
        MaestroBrand | None,
        Field(
            description="Exact brand name/colors/font_set/CTA overrides. Omit to inherit; an object replaces previous overrides and explicit null clears them."
        ),
    ] = None,
    website_url: Annotated[
        str | None,
        Field(
            description="Public website source captured by the service. Omit to reuse the original source; explicit null clears it.",
            max_length=2048,
        ),
    ] = None,
) -> str:
    """Create a complete video or iterate on a prior Maestro video.

    The call returns immediately with a task_id. Use maestro_get_task to monitor progress and obtain
    each completed language variant's output_url, captions_url, cover_url, duration, and QC score.
    """
    if action != "generate" and not ref_task_id:
        return f"Error: action={action} requires ref_task_id."
    if len(assets or []) + len(file_urls or []) > 20:
        return "Error: assets and file_urls support at most 20 combined items."

    payload: dict[str, Any] = {"prompt": prompt, "action": action}
    if ref_task_id:
        payload["ref_task_id"] = ref_task_id
    if aspect is not None:
        payload["aspect"] = aspect
    if duration is not None:
        payload["duration"] = duration
    if scenario is not None:
        payload["scenario"] = scenario
    if style is not None:
        payload["style"] = style
    if voice is not None:
        payload["voice"] = voice
    if file_urls is not None:
        payload["file_urls"] = file_urls
    if audio_mode is not None:
        payload["audio_mode"] = audio_mode
    if assets is not None:
        payload["assets"] = [asset.model_dump(exclude_none=True) for asset in assets]
    if _supplied("brand", brand):
        payload["brand"] = brand.model_dump(exclude_none=True) if brand is not None else None
    if _supplied("website_url", website_url):
        payload["website_url"] = website_url
    if langs:
        payload["langs"] = langs
    if callback_url:
        payload["callback_url"] = callback_url

    return format_submission_result(await client.create_video(payload))


def _supplied(field: str, value: object) -> bool:
    """Keep explicit JSON null distinct from an omitted optional MCP argument."""
    if value is not None:
        return True
    try:
        request = mcp.get_context().request_context.request
        arguments = getattr(getattr(request, "params", None), "arguments", None) or {}
        return field in arguments
    except (ValueError, LookupError, AttributeError):
        return False
