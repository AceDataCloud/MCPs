"""Informational tools for the reCAPTCHA API."""

from core.server import mcp


@mcp.tool()
async def recaptcha_get_usage_guide() -> str:
    """Get a usage guide for the reCAPTCHA tools."""
    return """# reCAPTCHA Usage Guide

Use `recaptcha2_recognize` for image grids, `recaptcha2_get_token` for v2 tokens, and `recaptcha3_get_token` for v3 tokens.
"""


@mcp.tool()
async def recaptcha_get_api_info() -> str:
    """Get API information for the reCAPTCHA service."""
    return """# reCAPTCHA API Information

Base URL: `https://api.acedata.cloud`
Endpoints:
- `POST /captcha/recognition/recaptcha2` with `image`, `question`, `async?`
- `POST /captcha/token/recaptcha2` with `website_key`, `website_url`, `proxy?`, `async?`
- `POST /captcha/token/recaptcha3` with `page_action`, `website_key`, `website_url`, `async?`
"""
