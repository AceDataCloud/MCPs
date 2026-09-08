"""Informational tools for the Localization API."""

from core.server import mcp


@mcp.tool()
async def localization_get_usage_guide() -> str:
    """Get a guide for using the Localization tools."""
    return """# Localization Tools Usage Guide

## Available Tools

### Translation
**localization_translate** - Translate Markdown or JSON localization input
- input: Markdown string for `md`, or JSON object for `json` (required)
- locale: Target locale (required)
- extension: `md` or `json` (required)
- model: Optional model, `gpt-3.5` or `gpt-4`

## Examples

```
localization_translate(
    input="# Title\n\nThis is a paragraph.",
    locale="de",
    extension="md",
)
```

```
localization_translate(
    input={"message.clickButton": {"message": "Please click button to apply"}},
    locale="zh-CN",
    extension="json",
    model="gpt-4",
)
```
"""


@mcp.tool()
async def localization_get_api_info() -> str:
    """Get information about the Localization API service."""
    return """# Localization API Information

| Property  | Value                         |
|-----------|-------------------------------|
| Service   | Localization translation      |
| Endpoint  | POST /localization/translate  |
| Base URL  | https://api.acedata.cloud     |
| Auth      | bearer token required         |

## Request Body
| Field     | Type            | Required | Notes                                  |
|-----------|-----------------|----------|----------------------------------------|
| input     | string or object| Yes      | String for md, object for json         |
| locale    | string          | Yes      | Target locale                          |
| extension | string          | Yes      | `md` or `json`                         |
| model     | string          | No       | `gpt-3.5` or `gpt-4`                   |
"""
