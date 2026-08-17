"""Captcha tools for the hCaptcha API."""

import json
from typing import Annotated, Literal

from pydantic import Field

from core.client import client
from core.exceptions import HCaptchaAPIError, HCaptchaAuthError
from core.server import mcp

TaskMode = Literal["sync", "async"]


@mcp.tool()
async def hcaptcha_recognize(
    queries: Annotated[
        list[str] | None, Field(description="Optional list of base64-encoded challenge tiles.")
    ] = None,
    question: Annotated[
        str | None, Field(description="Optional challenge question text shown by hCaptcha.")
    ] = None,
    mode: Annotated[
        TaskMode | None,
        Field(
            description="Processing mode. Defaults to API sync behavior; use 'async' to submit asynchronously."
        ),
    ] = None,
) -> str:
    """Recognize hCaptcha image challenges."""
    try:
        result = await client.recognize(queries=queries, question=question, mode=mode)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except HCaptchaAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except HCaptchaAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error recognizing hCaptcha", "message": str(e)})


@mcp.tool()
async def hcaptcha_get_token(
    website_key: Annotated[str, Field(description="The hCaptcha site key from the target page.")],
    website_url: Annotated[
        str, Field(description="The full URL of the page containing the widget.")
    ],
    rqdata: Annotated[
        str | None, Field(description="Optional hCaptcha rqdata value expected by the site.")
    ] = None,
    proxy: Annotated[
        str | None, Field(description="Optional proxy string to use while solving.")
    ] = None,
    mode: Annotated[
        TaskMode | None,
        Field(
            description="Processing mode. Defaults to API sync behavior; use 'async' to submit asynchronously."
        ),
    ] = None,
) -> str:
    """Get an hCaptcha token for a website."""
    if not website_key or not website_url:
        return json.dumps(
            {"error": "Validation Error", "message": "website_key and website_url are required"}
        )

    try:
        result = await client.get_token(
            website_key=website_key,
            website_url=website_url,
            rqdata=rqdata,
            proxy=proxy,
            mode=mode,
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    except HCaptchaAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except HCaptchaAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error getting hCaptcha token", "message": str(e)})
