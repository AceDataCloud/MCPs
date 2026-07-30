# MCP Turnstile Server

A Model Context Protocol (MCP) server for AceDataCloud's Turnstile captcha-solving APIs.

## Features
- Obtain Cloudflare Turnstile tokens and poll async task results.
- Shared async task polling via `/captcha/tasks`
- Bearer-token authentication through AceDataCloud

## Installation
```bash
pip install mcp-turnstile
```

## Configuration
```bash
export ACEDATACLOUD_API_TOKEN=your_token_here
export TURNSTILE_REQUEST_TIMEOUT=120
```

## Tools
- `turnstile_get_token` — Get a Cloudflare Turnstile token
- `turnstile_get_task` — Poll a Turnstile task result
- `turnstile_get_usage_guide` — Get Turnstile usage guide
- `turnstile_get_api_info` — Get Turnstile API information
