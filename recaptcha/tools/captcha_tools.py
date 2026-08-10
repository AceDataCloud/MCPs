"""Captcha tools for the reCAPTCHA API."""

import json
from typing import Annotated, Literal

from pydantic import Field

from core.client import client
from core.exceptions import ReCaptchaAPIError, ReCaptchaAuthError
from core.server import mcp

TaskMode = Literal["sync", "async"]


@mcp.tool()
async def recaptcha2_recognize(
    image: Annotated[str, Field(description="Base64-encoded reCAPTCHA v2 challenge image.")],
    question: Annotated[str, Field(description="Challenge question text shown to the user.")],
    mode: Annotated[TaskMode | None, Field(description="Processing mode. Defaults to API sync behavior; use 'async' to submit asynchronously.")] = None,
) -> str:
    """Recognize a reCAPTCHA v2 image challenge."""
    if not image or not question:
        return json.dumps({"error": "Validation Error", "message": "image and question are required"})
    try:
        result = await client.recognize2(image=image, question=question, mode=mode)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except ReCaptchaAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except ReCaptchaAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error recognizing reCAPTCHA", "message": str(e)})


@mcp.tool()
async def recaptcha2_get_token(
    website_key: Annotated[str, Field(description="The reCAPTCHA v2 site key from the target page.")],
    website_url: Annotated[str, Field(description="The full URL of the page containing the widget.")],
    proxy: Annotated[str | None, Field(description="Optional proxy string to use while solving.")] = None,
    mode: Annotated[TaskMode | None, Field(description="Processing mode. Defaults to API sync behavior; use 'async' to submit asynchronously.")] = None,
) -> str:
    """Get a reCAPTCHA v2 token."""
    if not website_key or not website_url:
        return json.dumps({"error": "Validation Error", "message": "website_key and website_url are required"})
    try:
        result = await client.get_token2(website_key=website_key, website_url=website_url, proxy=proxy, mode=mode)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except ReCaptchaAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except ReCaptchaAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error getting reCAPTCHA v2 token", "message": str(e)})


@mcp.tool()
async def recaptcha3_get_token(
    page_action: Annotated[str, Field(description="The reCAPTCHA v3 page action value expected by the site.")],
    website_key: Annotated[str, Field(description="The reCAPTCHA v3 site key from the target page.")],
    website_url: Annotated[str, Field(description="The full URL of the page containing the widget.")],
    mode: Annotated[TaskMode | None, Field(description="Processing mode. Defaults to API sync behavior; use 'async' to submit asynchronously.")] = None,
) -> str:
    """Get a reCAPTCHA v3 token."""
    if not page_action or not website_key or not website_url:
        return json.dumps({"error": "Validation Error", "message": "page_action, website_key, and website_url are required"})
    try:
        result = await client.get_token3(page_action=page_action, website_key=website_key, website_url=website_url, mode=mode)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except ReCaptchaAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except ReCaptchaAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error getting reCAPTCHA v3 token", "message": str(e)})
