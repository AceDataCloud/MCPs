"""Prompt templates for the Face Transform MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
"""

from core.server import mcp


@mcp.prompt()
def face_guide() -> str:
    """Guide for choosing the right Face Transform tool."""
    return """# Face Transform Guide

When the user wants to inspect or transform a face in a photo, pick the matching tool:

## Inspect faces
**Tool:** `face_detect_keypoints`
Detects 90+ keypoints per face. Useful for counting faces or feeding landmarks
into downstream animation / alignment.

## Beautify a portrait
**Tool:** `face_beautify`
Apply smoothing / whitening / face slimming / eye enlarging. Each parameter is
0-100; omit a parameter to use the API default.

## Age / de-age
**Tool:** `face_change_age`
The API picks the natural direction (older for a young portrait, younger for an
older portrait).

## Swap perceived gender
**Tool:** `face_change_gender`
Transforms facial gender characteristics on a portrait.

## Move one face onto another image
**Tool:** `face_swap`
`source_image_url` provides the face; `target_image_url` is the body / scene
that receives the new face. Optional `callback_url` enables async webhook
delivery for long-running jobs.

## Cartoonize a portrait
**Tool:** `face_cartoonize`
Generates an animated / cartoon-style rendering of the input portrait.

## Verify a live person
**Tool:** `face_detect_liveness`
Decide whether the image is a live capture vs a printed photo or screen
reshoot. Useful for KYC / anti-spoof workflows.

## Usage Guide
**Tool:** `face_get_usage_guide`
Returns the full tool inventory in one call. Useful when the model needs a
refresher.

## Notes
- All Face APIs are currently in Alpha — interfaces may evolve.
- Provide front-facing, clearly visible faces for best results.
- Bearer token authentication is required.
"""


@mcp.prompt()
def face_workflow_examples() -> str:
    """Common workflow examples for face analysis and transformation."""
    return """# Face Transform Workflow Examples

## 1. Count and locate faces in a group photo
1. Call `face_detect_keypoints(image_url=...)` with `mode=0` (default).
2. Inspect the returned `faces` array to count and locate each face.

## 2. Light retouch on a portrait
1. Call `face_beautify(image_url=..., smoothing=15, whitening=25)`.
2. Return the produced image URL to the user.

## 3. Replace a face in a scene
1. Call `face_swap(source_image_url=<headshot>, target_image_url=<scene>)`.
2. Optionally pass `callback_url` to receive the result via webhook.

## 4. Generate an avatar
1. Call `face_cartoonize(image_url=...)` on a clean portrait.
2. Display the cartoon avatar URL from the response.

## 5. KYC liveness check
1. Call `face_detect_liveness(image_url=<captured selfie>)`.
2. Reject the user if the response indicates a non-live source.

## Tips
- Use square, front-facing portraits for best beautify / age / gender output.
- `face_swap` works best when both faces are clearly visible and similarly sized.
- All endpoints return inline; only `face_swap` accepts an async `callback_url`.
"""
