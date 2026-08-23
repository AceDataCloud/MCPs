# MCP ReCaptcha Server

A Model Context Protocol (MCP) server for AceDataCloud's reCAPTCHA captcha-solving APIs.

## Features
- Solve reCAPTCHA image challenges and obtain reCAPTCHA v2/v3 tokens.
- Bearer-token authentication through AceDataCloud

## Installation
```bash
pip install mcp-recaptcha
```

## Configuration
```bash
export ACEDATACLOUD_API_TOKEN=your_token_here
export RECAPTCHA_REQUEST_TIMEOUT=120
```

## Tools
- `recaptcha2_recognize` — Recognize a reCAPTCHA v2 image challenge
- `recaptcha2_get_token` — Get a reCAPTCHA v2 token
- `recaptcha3_get_token` — Get a reCAPTCHA v3 token
- `recaptcha_get_usage_guide` — Get reCAPTCHA usage guide
- `recaptcha_get_api_info` — Get reCAPTCHA API information

## Service details

<!-- canonical-documentation -->
[Service details](https://platform.acedata.cloud/services/485cc5ca-7f1e-48e5-944e-1fe82b4637e8)
