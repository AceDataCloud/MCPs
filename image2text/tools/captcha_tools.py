"""Captcha tools for the Image2Text API."""

import json
from typing import Annotated, Literal

from pydantic import Field

from core.client import client
from core.exceptions import Image2TextAPIError, Image2TextAuthError
from core.server import mcp

TaskMode = Literal["sync", "async"]


@mcp.tool()
async def image2text_recognize(
    image: Annotated[str, Field(description="Base64-encoded image content to recognize.")],
    mode: Annotated[TaskMode | None, Field(description="Processing mode. Defaults to 'async'; use 'sync' to wait inline.")] = None,
) -> str:
    """Recognize text from a captcha-style image."""
    if not image:
        return json.dumps({"error": "Validation Error", "message": "image is required"})
    try:
        result = await client.recognize(image=image, mode=mode)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Image2TextAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except Image2TextAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error recognizing image text", "message": str(e)})
