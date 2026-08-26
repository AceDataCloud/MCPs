"""Captcha tools for the Turnstile API."""

import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import TurnstileAPIError, TurnstileAuthError
from core.server import mcp


@mcp.tool()
async def turnstile_get_token(
    website_key: Annotated[str, Field(description="The Turnstile site key from the target page.")],
    website_url: Annotated[
        str, Field(description="The full URL of the page containing the widget.")
    ],
    action: Annotated[
        str | None, Field(description="Optional Turnstile action value expected by the site.")
    ] = None,
    cdata: Annotated[
        str | None, Field(description="Optional Turnstile cData value expected by the site.")
    ] = None,
    async_: Annotated[
        bool | None,
        Field(alias="async", description="Whether to submit the token task asynchronously."),
    ] = None,
) -> str:
    """Get a Cloudflare Turnstile token."""
    if not website_key or not website_url:
        return json.dumps(
            {"error": "Validation Error", "message": "website_key and website_url are required"}
        )
    try:
        result = await client.get_token(
            website_key=website_key,
            website_url=website_url,
            action=action,
            cdata=cdata,
            async_=async_,
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    except TurnstileAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except TurnstileAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error getting Turnstile token", "message": str(e)})
