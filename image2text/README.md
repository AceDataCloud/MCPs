# MCP Image2Text Server

A Model Context Protocol (MCP) server for AceDataCloud's Image2Text captcha-solving APIs.

## Features
- Recognize text from base64-encoded captcha or challenge images.
- Shared async task polling via `/captcha/tasks`
- Bearer-token authentication through AceDataCloud

## Installation
```bash
pip install mcp-image2text
```

## Configuration
```bash
export ACEDATACLOUD_API_TOKEN=your_token_here
export IMAGE2TEXT_REQUEST_TIMEOUT=120
```

## Tools
- `image2text_recognize` — Recognize text from an image
- `image2text_get_task` — Poll an image2text task result
- `image2text_get_usage_guide` — Get image2text usage guide
- `image2text_get_api_info` — Get image2text API information
