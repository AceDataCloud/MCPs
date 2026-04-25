# OpenAIMCP

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for OpenAI API access using [AceDataCloud](https://platform.acedata.cloud).

Interact with OpenAI models for chat completions, image generation, text embeddings, and more — directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Chat Completions** — Access GPT-4, GPT-4o, GPT-5, o1, o3, o4-mini, and many more models
- **Responses API** — Extended model variant support including dated releases and search-preview models
- **Image Generation** — Create images with gpt-image-1, gpt-image-2, dall-e-3, and nano-banana models
- **Image Editing** — Modify existing images with AI
- **Text Embeddings** — Generate vector representations with text-embedding-3 models

## Quick Start

### Prerequisites

Get an API token from [AceDataCloud](https://platform.acedata.cloud).

### Installation

```bash
pip install mcp-openai
```

### Configuration

Set your API token:

```bash
export ACEDATACLOUD_API_TOKEN=your_api_token_here
```

### Run

```bash
mcp-openai
```

## Available Tools

| Tool | Description |
|------|-------------|
| `openai_chat_completion` | Create chat completions using OpenAI models |
| `openai_create_response` | Create responses using the Responses API |
| `openai_generate_image` | Generate images from text descriptions |
| `openai_edit_image` | Edit existing images with AI |
| `openai_create_embedding` | Create text embedding vectors |
| `openai_list_chat_models` | List available chat/completion models |
| `openai_list_image_models` | List available image models |
| `openai_list_embedding_models` | List available embedding models |
| `openai_get_usage_guide` | Get comprehensive usage guide |

## Supported Models

### Chat Completion Models
- **GPT-5 Series**: gpt-5.5, gpt-5.5-pro, gpt-5.4, gpt-5.4-pro, gpt-5.2, gpt-5.1, gpt-5, gpt-5-mini, gpt-5-nano
- **GPT-4 Series**: gpt-4.1, gpt-4.1-mini, gpt-4.1-nano, gpt-4o, gpt-4o-mini, gpt-4
- **Reasoning**: o4-mini, o3, o3-mini, o3-pro, o1, o1-mini, o1-pro

### Image Models
- gpt-image-1, gpt-image-1.5, gpt-image-2, dall-e-3, nano-banana, nano-banana-2, nano-banana-pro

### Embedding Models
- text-embedding-3-small, text-embedding-3-large, text-embedding-ada-002

## Usage Examples

### Chat Completion

```
openai_chat_completion(
    messages=[{"role": "user", "content": "Explain quantum computing in simple terms"}],
    model="gpt-4.1"
)
```

### Image Generation

```
openai_generate_image(
    prompt="A serene Japanese garden with cherry blossoms at sunset, photorealistic",
    model="gpt-image-1",
    size="1024x1024"
)
```

### Text Embeddings

```
openai_create_embedding(
    input="The quick brown fox jumps over the lazy dog",
    model="text-embedding-3-small"
)
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API token (required) | — |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `OPENAI_REQUEST_TIMEOUT` | Request timeout in seconds | `60` |
| `MCP_SERVER_NAME` | MCP server name | `openai` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Development

```bash
# Install dependencies
pip install -e ".[dev,test]"

# Run tests
pytest

# Run linter
ruff check .
```

## API Reference

- [AceDataCloud Platform](https://platform.acedata.cloud)
- [OpenAI API Documentation](https://platform.openai.com/docs)

## License

MIT
