# MCP Gemini Server

A Model Context Protocol (MCP) server for Gemini AI via the AceDataCloud platform.
Supports all Gemini models including Gemini 2.0, 2.5, 3.0, and 3.1.

## Features

- **Gemini Chat Completion** (OpenAI-compatible format)
- **Gemini Generate Content** (Native Gemini API format)
- All Gemini models supported

## Installation

```bash
pip install mcp-gemini
```

## Configuration

Copy `.env.example` to `.env` and set your API token:

```bash
ACEDATACLOUD_API_TOKEN=your_api_token_here
```

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud).

## Usage

```bash
mcp-gemini
```

## Available Tools

- `gemini_chat_completion` - Chat with Gemini using OpenAI-compatible format
- `gemini_generate_content` - Generate content using native Gemini API
- `gemini_list_models` - List all available Gemini models

## Supported Models

| Model | Description |
|-------|-------------|
| gemini-2.5-flash | Gemini 2.5 Flash (recommended default) |
| gemini-2.5-pro | Gemini 2.5 Pro |
| gemini-2.0-flash | Gemini 2.0 Flash |
| gemini-3-flash-preview | Gemini 3 Flash Preview |
| gemini-3.0-pro | Gemini 3.0 Pro |
| gemini-3.1-pro | Gemini 3.1 Pro (latest) |

## License

MIT
