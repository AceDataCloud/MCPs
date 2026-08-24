"""Captcha tools for the Image2Text API."""

import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import Image2TextAPIError, Image2TextAuthError
from core.server import mcp


@mcp.tool()
async def image2text_recognize(
    image: Annotated[str, Field(description="Base64-encoded image content to recognize.")],
    async_: Annotated[
        bool | None,
        Field(alias="async", description="Whether to process the request asynchronously."),
    ] = None,
) -> str:
    """Recognize text from a captcha-style image."""
    if not image:
        return json.dumps({"error": "Validation Error", "message": "image is required"})
    try:
        result = await client.recognize(image=image, async_=async_)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Image2TextAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except Image2TextAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error recognizing image text", "message": str(e)})
