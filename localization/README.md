# MCP Localization Server

A Model Context Protocol (MCP) server for AceDataCloud's Localization translation API.

## Features
- Translate Markdown strings or JSON localization objects.
- Supports the locales, models, and `/localization/translate` endpoint from the OpenAPI spec.
- Bearer-token authentication through AceDataCloud.

## Installation
```bash
pip install mcp-localization
```

## Configuration
```bash
export ACEDATACLOUD_API_TOKEN=your_token_here
export LOCALIZATION_REQUEST_TIMEOUT=120
```

## Tools
- `localization_translate` — Translate Markdown or JSON localization input
- `localization_get_usage_guide` — Get localization usage guide
- `localization_get_api_info` — Get localization API information

## Service details

<!-- canonical-documentation -->
[Service details](https://platform.acedata.cloud/documents/localization-translate)
