# MCP Grok Server

A Model Context Protocol (MCP) server for Grok AI via the AceDataCloud platform.
Supports all Grok models including Grok 3, Grok 4, and specialized variants.

## Features

- **Grok Chat Completion** (OpenAI-compatible format)
- All Grok models supported

## Installation

```bash
pip install mcp-grok
```

## Configuration

Copy `.env.example` to `.env` and set your API token:

```bash
ACEDATACLOUD_API_TOKEN=your_api_token_here
```

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud).

## Usage

```bash
mcp-grok
```

## Available Tools

- `grok_chat_completion` - Chat with Grok models
- `grok_list_models` - List all available Grok models

## Supported Models

| Model | Description |
|-------|-------------|
| grok-3 | Grok 3 (recommended default) |
| grok-3-mini | Grok 3 Mini |
| grok-4 | Grok 4 (latest) |
| grok-4-1-fast | Grok 4.1 Fast |
| grok-4-1-fast-non-reasoning | Grok 4.1 Fast (non-reasoning) |
| grok-2-vision | Grok 2 Vision |

## License

MIT
