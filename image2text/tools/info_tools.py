"""Informational tools for the Image2Text API."""

from core.server import mcp


@mcp.tool()
async def image2text_get_usage_guide() -> str:
    """Get a usage guide for the image2text tools."""
    return """# Image2Text Usage Guide

Use `image2text_recognize` with a base64 image. The tool supports the documented
sync/async submission mode for `/captcha/recognition/image2text`.
"""


@mcp.tool()
async def image2text_get_api_info() -> str:
    """Get API information for the image2text service."""
    return """# Image2Text API Information

Base URL: `https://api.acedata.cloud`
Endpoints:
- `POST /captcha/recognition/image2text` with `image`, `async?`
- `POST /captcha/tasks` with `task_id`

Ready responses may include `text` and `elapsed`.
"""
