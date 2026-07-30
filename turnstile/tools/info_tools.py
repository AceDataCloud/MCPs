"""Informational tools for the Turnstile API."""

from core.server import mcp


@mcp.tool()
async def turnstile_get_usage_guide() -> str:
    """Get a usage guide for the Turnstile tools."""
    return """# Turnstile Usage Guide

Use `turnstile_get_token` to request a Turnstile token. Default mode is async; poll returned tasks with `turnstile_get_task`.
"""


@mcp.tool()
async def turnstile_get_api_info() -> str:
    """Get API information for the Turnstile service."""
    return """# Turnstile API Information

Base URL: `https://api.acedata.cloud`
Endpoints:
- `POST /captcha/token/turnstile` with `website_key`, `website_url`, `action?`, `cdata?`, `async?`
- `POST /captcha/tasks` with `task_id`

Ready responses may include `token` and `elapsed`.
"""
