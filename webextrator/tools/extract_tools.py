"""Extract and render tools for WebExtrator API."""

import json
from typing import Annotated, Any, cast

from pydantic import Field

from core.client import client
from core.exceptions import WebExtraterAPIError, WebExtraterAuthError
from core.server import mcp
from core.types import BlockResource, ExpectedType, TaskMode, WaitUntil


@mcp.tool()
async def webextrator_extract(
    url: Annotated[
        str,
        Field(description="The URL of the web page to extract content from. Required."),
    ],
    expected_type: Annotated[
        ExpectedType | None,
        Field(
            description=(
                "Hint about expected page type. Options: 'product', 'article', 'general'. "
                "Helps the extractor optimize for the content structure."
            )
        ),
    ] = None,
    enable_llm: Annotated[
        bool | None,
        Field(
            description=(
                "Enable LLM-based semantic normalization for richer structured output. "
                "Default is false."
            )
        ),
    ] = None,
    wait_until: Annotated[
        WaitUntil | None,
        Field(
            description=(
                "Page load wait condition before extracting. Options: 'load', "
                "'domcontentloaded', 'networkidle', 'commit'. Default is 'networkidle'."
            )
        ),
    ] = None,
    timeout: Annotated[
        float | None,
        Field(description="Total timeout in seconds for page load. Default is 30."),
    ] = None,
    delay: Annotated[
        float | None,
        Field(description="Extra delay in seconds after page load before extracting."),
    ] = None,
    wait_for_selector: Annotated[
        str | None,
        Field(description="CSS selector to wait for before extracting content."),
    ] = None,
    block_resources: Annotated[
        list[BlockResource] | None,
        Field(
            description=(
                "Resource types to block during page load to speed up rendering. "
                "Options: 'image', 'font', 'media', 'stylesheet', 'xhr', 'fetch'."
            )
        ),
    ] = None,
    headers: Annotated[
        dict[str, str] | None,
        Field(description="Extra HTTP headers to include with the page request."),
    ] = None,
    user_agent: Annotated[
        str | None,
        Field(description="Override the User-Agent header for the page request."),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(
            description=(
                "Callback URL for async processing. If provided, the task runs asynchronously "
                "and results are sent to this URL when complete."
            )
        ),
    ] = None,
    cookies: Annotated[
        list[dict[str, Any]] | None,
        Field(
            description=(
                "Cookies to install before navigation. Each cookie is an object with at least "
                "'name' and 'value', plus optional 'domain', 'path', 'expires', 'httpOnly', "
                "'secure', 'sameSite'. Useful for authenticated pages."
            )
        ),
    ] = None,
    bypass_cache: Annotated[
        bool | None,
        Field(
            description=(
                "Skip the Redis result cache for this request (still writes the fresh result "
                "back). Default is false."
            )
        ),
    ] = None,
    cache_ttl_seconds: Annotated[
        float | None,
        Field(
            description=(
                "Override the global cache TTL (seconds) for this entry. 0 means do not cache "
                "this response. Default is 3600."
            )
        ),
    ] = None,
    mode: Annotated[
        TaskMode | None,
        Field(
            description=(
                "Processing mode. 'sync' (default) waits for the result; 'async' returns "
                "immediately with a task_id to poll via the Tasks API."
            )
        ),
    ] = None,
) -> str:
    """Extract structured content from a web page using the WebExtrator API.

    Navigates to the specified URL, renders the page, and extracts structured data
    such as product details, article content, or general page information.

    Use this when:
    - You need to extract structured data from a web page
    - You want product details, article content, or general page data
    - You need LLM-enhanced semantic normalization of extracted content

    Returns:
        JSON response containing the extracted structured content.
    """
    if not url:
        return json.dumps({"error": "Validation Error", "message": "url is required"})

    try:
        result = await client.extract(
            url=url,
            expected_type=expected_type,
            enable_llm=enable_llm,
            wait_until=wait_until,
            timeout=timeout,
            delay=delay,
            wait_for_selector=wait_for_selector,
            block_resources=cast(list[str] | None, block_resources),
            headers=headers,
            user_agent=user_agent,
            callback_url=callback_url,
            cookies=cookies,
            bypass_cache=bypass_cache,
            cache_ttl_seconds=cache_ttl_seconds,
            mode=mode,
        )

        if not result:
            return json.dumps({"error": "No response received from the API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except WebExtraterAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except WebExtraterAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error extracting content", "message": str(e)})


@mcp.tool()
async def webextrator_render(
    url: Annotated[
        str,
        Field(description="The URL of the web page to render. Required."),
    ],
    wait_until: Annotated[
        WaitUntil | None,
        Field(
            description=(
                "Page load wait condition before capturing HTML. Options: 'load', "
                "'domcontentloaded', 'networkidle', 'commit'. Default is 'networkidle'."
            )
        ),
    ] = None,
    timeout: Annotated[
        float | None,
        Field(description="Total timeout in seconds for page load. Default is 30."),
    ] = None,
    delay: Annotated[
        float | None,
        Field(description="Extra delay in seconds after page load before capturing HTML."),
    ] = None,
    wait_for_selector: Annotated[
        str | None,
        Field(description="CSS selector to wait for before capturing HTML."),
    ] = None,
    block_resources: Annotated[
        list[BlockResource] | None,
        Field(
            description=(
                "Resource types to block during page load to speed up rendering. "
                "Options: 'image', 'font', 'media', 'stylesheet', 'xhr', 'fetch'."
            )
        ),
    ] = None,
    headers: Annotated[
        dict[str, str] | None,
        Field(description="Extra HTTP headers to include with the page request."),
    ] = None,
    user_agent: Annotated[
        str | None,
        Field(description="Override the User-Agent header for the page request."),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(
            description=(
                "Callback URL for async processing. If provided, the task runs asynchronously "
                "and results are sent to this URL when complete."
            )
        ),
    ] = None,
    cookies: Annotated[
        list[dict[str, Any]] | None,
        Field(
            description=(
                "Cookies to install before navigation. Each cookie is an object with at least "
                "'name' and 'value', plus optional 'domain', 'path', 'expires', 'httpOnly', "
                "'secure', 'sameSite'. Useful for authenticated pages."
            )
        ),
    ] = None,
    bypass_cache: Annotated[
        bool | None,
        Field(
            description=(
                "Skip the Redis result cache for this request (still writes the fresh result "
                "back). Default is false."
            )
        ),
    ] = None,
    cache_ttl_seconds: Annotated[
        float | None,
        Field(
            description=(
                "Override the global cache TTL (seconds) for this entry. 0 means do not cache "
                "this response. Default is 3600."
            )
        ),
    ] = None,
    mode: Annotated[
        TaskMode | None,
        Field(
            description=(
                "Processing mode. 'sync' (default) waits for the result; 'async' returns "
                "immediately with a task_id to poll via the Tasks API."
            )
        ),
    ] = None,
) -> str:
    """Render a web page and return the fully rendered HTML.

    Uses a headless browser to navigate to the specified URL, waits for JavaScript
    to execute, and returns the final rendered HTML source.

    Use this when:
    - You need the fully rendered HTML of a JavaScript-heavy page
    - You want to inspect the DOM after dynamic content has loaded
    - You need to capture single-page application (SPA) content

    Returns:
        JSON response containing the rendered HTML content.
    """
    if not url:
        return json.dumps({"error": "Validation Error", "message": "url is required"})

    try:
        result = await client.render(
            url=url,
            wait_until=wait_until,
            timeout=timeout,
            delay=delay,
            wait_for_selector=wait_for_selector,
            block_resources=cast(list[str] | None, block_resources),
            headers=headers,
            user_agent=user_agent,
            callback_url=callback_url,
            cookies=cookies,
            bypass_cache=bypass_cache,
            cache_ttl_seconds=cache_ttl_seconds,
            mode=mode,
        )

        if not result:
            return json.dumps({"error": "No response received from the API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except WebExtraterAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except WebExtraterAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error rendering page", "message": str(e)})
