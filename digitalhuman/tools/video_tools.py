"""Video generation tools for Digital Human."""

import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import DigitalHumanAPIError, DigitalHumanAuthError
from core.server import mcp
from core.types import (
    DEFAULT_ENGINE,
    DEFAULT_GUIDANCE,
    DEFAULT_RESOLUTION,
    DEFAULT_SEAM_FIX,
    DEFAULT_SPEED,
    DEFAULT_STEPS,
    DigitalHumanEngine,
    DigitalHumanResolution,
)
from core.utils import format_video_result


@mcp.tool()
async def digitalhuman_create_video(
    video_url: Annotated[
        str | None,
        Field(
            description=(
                "Public URL of the source face video. Supply either video_url or image_url."
            )
        ),
    ] = None,
    image_url: Annotated[
        str | None,
        Field(
            description=(
                "Public URL of the source face photo. Supply either image_url or video_url."
            )
        ),
    ] = None,
    audio_url: Annotated[
        str | None,
        Field(
            description="Public URL of the driving audio (.wav/.mp3/.m4a). Or provide text and voice_id."
        ),
    ] = None,
    text: Annotated[
        str | None,
        Field(description="Spoken text for TTS generation. Requires voice_id when provided."),
    ] = None,
    voice_id: Annotated[
        str | None,
        Field(description="Cloned voice ID returned by digitalhuman_clone_voice."),
    ] = None,
    engine: Annotated[
        DigitalHumanEngine,
        Field(
            description=(
                "Deprecated engine selector retained for backward compatibility. "
                "Options: latentsync or heygem."
            )
        ),
    ] = DEFAULT_ENGINE,
    guidance: Annotated[
        float,
        Field(description="Lip-sync strength for LatentSync. Lower values loosen sync."),
    ] = DEFAULT_GUIDANCE,
    steps: Annotated[
        int,
        Field(description="Diffusion steps for LatentSync."),
    ] = DEFAULT_STEPS,
    seam_fix: Annotated[
        bool,
        Field(description="Apply the mouth-seam reduction blend."),
    ] = DEFAULT_SEAM_FIX,
    speed: Annotated[
        float,
        Field(description="Audio tempo multiplier."),
    ] = DEFAULT_SPEED,
    resolution: Annotated[
        DigitalHumanResolution,
        Field(
            description="Deprecated resolution selector retained for backward compatibility. 720p or 540p."
        ),
    ] = DEFAULT_RESOLUTION,
    callback_url: Annotated[
        str | None,
        Field(description="Optional webhook URL for asynchronous completion."),
    ] = None,
    async_: Annotated[
        bool | None,
        Field(alias="async", description="Whether to return immediately with a task_id."),
    ] = None,
) -> str:
    """Create a digital human video from a face video or still image."""
    if bool(video_url) == bool(image_url):
        return json.dumps(
            {
                "error": "Validation Error",
                "message": "Provide exactly one of video_url or image_url.",
            }
        )
    if audio_url and text:
        return json.dumps(
            {
                "error": "Validation Error",
                "message": "Provide either audio_url or text, not both.",
            }
        )
    if text and not voice_id:
        return json.dumps(
            {
                "error": "Validation Error",
                "message": "voice_id is required when text is provided.",
            }
        )
    if not audio_url and not text:
        return json.dumps(
            {
                "error": "Validation Error",
                "message": "Provide either audio_url or text with voice_id.",
            }
        )

    payload = {
        "video_url": video_url,
        "image_url": image_url,
        "audio_url": audio_url,
        "text": text,
        "voice_id": voice_id,
        "engine": engine,
        "guidance": guidance,
        "steps": steps,
        "seam_fix": seam_fix,
        "speed": speed,
        "resolution": resolution,
        "callback_url": callback_url,
        "async": async_,
    }

    try:
        return format_video_result(await client.create_video(payload))
    except DigitalHumanAuthError as exc:
        return json.dumps({"error": "Authentication Error", "message": exc.message})
    except DigitalHumanAPIError as exc:
        return json.dumps({"error": "API Error", "message": exc.message})
    except Exception as exc:
        return json.dumps({"error": "Error creating video", "message": str(exc)})
