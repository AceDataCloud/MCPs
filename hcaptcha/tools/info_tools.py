"""Informational tools for the hCaptcha API."""

from core.server import mcp


@mcp.tool()
async def hcaptcha_get_usage_guide() -> str:
    """Get a usage guide for the hCaptcha tools."""
    return """# hCaptcha Usage Guide

Use `hcaptcha_recognize` for image selection challenges, `hcaptcha_get_token` for widget tokens, and `hcaptcha_get_task` to poll submissions created with `async=true`. Requests run synchronously by default.
"""


@mcp.tool()
async def hcaptcha_get_api_info() -> str:
    """Get API information for the hCaptcha service."""
    return """# hCaptcha API Information

Base URL: `https://api.acedata.cloud`
Endpoints:
- `POST /captcha/recognition/hcaptcha` with `queries?`, `question?`, `async?`
- `POST /captcha/token/hcaptcha` with `website_key`, `website_url`, `rqdata?`, `proxy?`, `async?`
- `POST /captcha/tasks` with `task_id`

Ready responses may include `solution`, `token`, `text`, and timing fields such as `started_at`, `finished_at`, and `elapsed`. Task polling can also return a terminal timeout response with `success: false`, `code: timeout`, and `status: failed`; stop polling that task if this happens.
"""
