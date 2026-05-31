"""Face analysis and transformation tools."""

import json
from collections.abc import Awaitable, Callable
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.exceptions import FaceAPIError, FaceAuthError
from core.server import mcp
from core.types import (
    DEFAULT_ANALYZE_MODE,
    DEFAULT_MODEL_VERSION,
    FaceAnalyzeMode,
    FaceModelVersion,
    FaceRotateDetection,
)


def _json_error(error: str, message: str) -> str:
    return json.dumps({"error": error, "message": message})


async def _call(
    method: Callable[..., Awaitable[dict[str, Any] | None]],
    **payload: Any,
) -> str:
    """Wrap a FaceClient call, returning a JSON string and mapping errors."""
    try:
        result = await method(**payload)
        if not result:
            return _json_error("Empty Response", "No response received from the API.")
        return json.dumps(result, ensure_ascii=False, indent=2)
    except FaceAuthError as e:
        return _json_error("Authentication Error", e.message)
    except FaceAPIError as e:
        return _json_error("API Error", e.message)
    except Exception as e:  # noqa: BLE001
        return _json_error("Request Failed", str(e))


@mcp.tool()
async def face_detect_keypoints(
    image_url: Annotated[
        str,
        Field(description="URL of the image containing one or more faces."),
    ],
    mode: Annotated[
        FaceAnalyzeMode,
        Field(description="0 = all faces (default), 1 = largest face only."),
    ] = DEFAULT_ANALYZE_MODE,
    face_model_version: Annotated[
        FaceModelVersion,
        Field(description="Algorithm version. '3.0' is recommended."),
    ] = DEFAULT_MODEL_VERSION,
    need_rotate_detection: Annotated[
        FaceRotateDetection,
        Field(description="0 = disabled (default), 1 = enabled."),
    ] = 0,
) -> str:
    """Detect faces in an image and return 90+ keypoints per face.

    Use this when:
    - You want raw landmark coordinates for downstream alignment / animation.
    - You need to count or locate faces in a photo.
    """
    if not image_url:
        return _json_error("Validation Error", "image_url is required")

    return await _call(
        client.analyze,
        image_url=image_url,
        mode=mode,
        face_model_version=face_model_version,
        need_rotate_detection=need_rotate_detection,
    )


@mcp.tool()
async def face_beautify(
    image_url: Annotated[
        str,
        Field(description="URL of the portrait to beautify."),
    ],
    smoothing: Annotated[
        int | None,
        Field(description="Skin smoothing 0-100 (default 10).", ge=0, le=100),
    ] = None,
    whitening: Annotated[
        int | None,
        Field(description="Whitening 0-100 (default 30).", ge=0, le=100),
    ] = None,
    face_lifting: Annotated[
        int | None,
        Field(description="Face slimming 0-100 (default 70).", ge=0, le=100),
    ] = None,
    eye_enlarging: Annotated[
        int | None,
        Field(description="Eye enlarging 0-100 (default 70).", ge=0, le=100),
    ] = None,
) -> str:
    """Apply beauty effects (smoothing / whitening / slimming / eye enlarging)."""
    if not image_url:
        return _json_error("Validation Error", "image_url is required")

    payload: dict = {"image_url": image_url}
    for key, value in {
        "smoothing": smoothing,
        "whitening": whitening,
        "face_lifting": face_lifting,
        "eye_enlarging": eye_enlarging,
    }.items():
        if value is not None:
            payload[key] = value

    return await _call(client.beautify, **payload)


@mcp.tool()
async def face_change_age(
    image_url: Annotated[
        str,
        Field(description="URL of the portrait to age-transform."),
    ],
) -> str:
    """Age or de-age a face. The API decides direction based on the input portrait."""
    if not image_url:
        return _json_error("Validation Error", "image_url is required")
    return await _call(client.change_age, image_url=image_url)


@mcp.tool()
async def face_change_gender(
    image_url: Annotated[
        str,
        Field(description="URL of the portrait whose facial gender should be swapped."),
    ],
) -> str:
    """Swap perceived facial gender characteristics in a portrait."""
    if not image_url:
        return _json_error("Validation Error", "image_url is required")
    return await _call(client.change_gender, image_url=image_url)


@mcp.tool()
async def face_swap(
    source_image_url: Annotated[
        str,
        Field(description="URL of the image whose face will be transplanted."),
    ],
    target_image_url: Annotated[
        str,
        Field(description="URL of the image that will receive the new face."),
    ],
    callback_url: Annotated[
        str | None,
        Field(description="Optional webhook URL to receive the result asynchronously."),
    ] = None,
    timeout: Annotated[
        int | None,
        Field(description="Max upstream wait time in seconds (default 120).", ge=1),
    ] = None,
) -> str:
    """Replace the face in `target_image_url` with the face from `source_image_url`."""
    if not source_image_url:
        return _json_error("Validation Error", "source_image_url is required")
    if not target_image_url:
        return _json_error("Validation Error", "target_image_url is required")

    payload: dict = {
        "source_image_url": source_image_url,
        "target_image_url": target_image_url,
    }
    if callback_url:
        payload["callback_url"] = callback_url
    if timeout is not None:
        payload["timeout"] = timeout

    return await _call(client.swap, **payload)


@mcp.tool()
async def face_cartoonize(
    image_url: Annotated[
        str,
        Field(description="URL of the portrait to stylize."),
    ],
) -> str:
    """Convert a portrait to an animated / cartoon style."""
    if not image_url:
        return _json_error("Validation Error", "image_url is required")
    return await _call(client.cartoon, image_url=image_url)


@mcp.tool()
async def face_detect_liveness(
    image_url: Annotated[
        str,
        Field(description="URL of the face image to verify."),
    ],
) -> str:
    """Decide whether a face image is from a live person versus a printed / screen photo."""
    if not image_url:
        return _json_error("Validation Error", "image_url is required")
    return await _call(client.detect_live, image_url=image_url)


@mcp.tool()
async def face_get_usage_guide() -> str:
    """Return a concise usage guide for the Face Transform tools.

    Use this when:
    - The model needs a refresher on which face tool fits the user's intent.
    - Onboarding a new conversation that hasn't seen the prompts yet.
    """
    return """# Face Transform Tools Usage Guide

## Available Tools

| Tool | Endpoint | Purpose |
|------|----------|---------|
| `face_detect_keypoints` | POST /face/analyze | Detect 90+ keypoints per face |
| `face_beautify` | POST /face/beautify | Smoothing / whitening / slimming / eye enlarging |
| `face_change_age` | POST /face/change-age | Age / de-age a face |
| `face_change_gender` | POST /face/change-gender | Swap facial gender characteristics |
| `face_swap` | POST /face/swap | Move source face onto target image |
| `face_cartoonize` | POST /face/cartoon | Convert portrait to cartoon style |
| `face_detect_liveness` | POST /face/detect-live | Detect live vs printed/screen face |

## Notes
- All endpoints return results synchronously and include URLs of generated images.
- `face_swap` accepts an optional `callback_url` for async webhook delivery.
- All APIs are currently in Alpha — interfaces may evolve.
- Provide front-facing, clearly visible faces for best results.
"""
