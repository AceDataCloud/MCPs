"""ShortURL tools for URL shortening API."""

import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import ShortURLAPIError, ShortURLAuthError
from core.server import mcp


@mcp.tool()
async def shorturl_create(
    url: Annotated[
        str,
        Field(description="The long URL to shorten. Must be a valid HTTP or HTTPS URL. Required."),
    ],
) -> str:
    """Create a short URL from a long URL.

    Converts a long URL into a short, easy-to-share URL using the ShortURL API.
    The short URL redirects to the original long URL when visited.

    This is useful for:
    - Sharing links on social media with character limits
    - Creating clean, memorable links for marketing
    - Tracking link clicks and engagement
    - Making long URLs more manageable in documents and messages

    Args:
        url: The long URL to shorten. Must be a valid HTTP or HTTPS URL.

    Returns:
        JSON response containing the shortened URL.

    Example:
        shorturl_create(url="https://platform.acedata.cloud/documents/a2303356-6672-4eb8-9778-75f55c998fe9")
    """
    if not url:
        return json.dumps({"error": "Validation Error", "message": "URL is required"})

    if not url.startswith(("http://", "https://")):
        return json.dumps(
            {
                "error": "Validation Error",
                "message": "URL must start with http:// or https://",
            }
        )

    try:
        result = await client.shorten(content=url)

        if not result:
            return json.dumps({"error": "No response received from the API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except ShortURLAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except ShortURLAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating short URL", "message": str(e)})


@mcp.tool()
async def shorturl_batch_create(
    urls: Annotated[
        list[str],
        Field(
            description="A list of long URLs to shorten. Each must be a valid HTTP or HTTPS URL. Maximum 10 URLs per batch."
        ),
    ],
) -> str:
    """Create short URLs for multiple long URLs in a single batch.

    Shortens multiple URLs at once, returning a mapping of original URLs
    to their shortened versions. Useful for bulk URL shortening tasks.

    Args:
        urls: A list of long URLs to shorten (max 10 per batch).

    Returns:
        JSON response containing the mapping of original to shortened URLs.

    Example:
        shorturl_batch_create(urls=["https://example.com/long-url-1", "https://example.com/long-url-2"])
    """
    if not urls:
        return json.dumps({"error": "Validation Error", "message": "URLs list is required"})

    if len(urls) > 10:
        return json.dumps(
            {
                "error": "Validation Error",
                "message": "Maximum 10 URLs per batch. Please split into smaller batches.",
            }
        )

    results = []
    for url in urls:
        if not url.startswith(("http://", "https://")):
            results.append(
                {
                    "original_url": url,
                    "short_url": None,
                    "error": "URL must start with http:// or https://",
                }
            )
            continue

        try:
            result = await client.shorten(content=url)
            short_url = result.get("data", {}).get("url", "") if result.get("success") else None
            entry: dict = {"original_url": url, "short_url": short_url}
            if not short_url:
                entry["error"] = result.get("error", {}).get("message", "Unknown error")
            results.append(entry)
        except ShortURLAuthError as e:
            results.append({"original_url": url, "short_url": None, "error": e.message})
            break  # Auth errors affect all subsequent requests
        except (ShortURLAPIError, Exception) as e:
            msg = e.message if hasattr(e, "message") else str(e)
            results.append({"original_url": url, "short_url": None, "error": msg})

    successful = sum(1 for r in results if r.get("short_url"))
    return json.dumps(
        {
            "total": len(urls),
            "successful": successful,
            "failed": len(urls) - successful,
            "results": results,
        },
        ensure_ascii=False,
        indent=2,
    )
