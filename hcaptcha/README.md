# MCP HCaptcha Server

A Model Context Protocol (MCP) server for AceDataCloud's hCaptcha captcha-solving APIs.

## Features
- Solve hCaptcha image challenges and retrieve hCaptcha site tokens.
- Shared async task polling via `/captcha/tasks`
- Bearer-token authentication through AceDataCloud

## Installation
```bash
pip install mcp-hcaptcha
```

## Configuration
```bash
export ACEDATACLOUD_API_TOKEN=your_token_here
export HCAPTCHA_REQUEST_TIMEOUT=120
```

## Tools
- `hcaptcha_recognize` — Recognize hCaptcha image challenges
- `hcaptcha_get_token` — Get an hCaptcha token for a website, optionally with `rqdata`
- `hcaptcha_get_task` — Poll a captcha task result
- `hcaptcha_get_usage_guide` — Get hCaptcha usage guide
- `hcaptcha_get_api_info` — Get hCaptcha API information

## Service details

<!-- canonical-documentation -->
[Service details](https://platform.acedata.cloud/services/018c653e-4f1b-433f-82f9-732ef2767040)
