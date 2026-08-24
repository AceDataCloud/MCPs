# Qwen Image MCP Server

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/qwen-image)

Model Context Protocol server for Qwen Image 3 generation and editing through Ace Data Cloud.

## Install

```bash
pip install mcp-qwen-image
export ACEDATACLOUD_API_TOKEN=your_token
mcp-qwen-image
```

Hosted MCP: `https://qwen-image.mcp.acedata.cloud/mcp`

## Tools

| Tool | Purpose |
|---|---|
| `qwen_image_generate` | Generate 1–6 images from text |
| `qwen_image_edit` | Edit with 1–3 reference images |
| `qwen_image_get_task` | Query one asynchronous task |
| `qwen_image_get_tasks_batch` | Query multiple tasks |
| `qwen_image_list_models` | Compare Standard and Pro |

Models: `qwen-image-3.0` (default) and `qwen-image-3.0-pro`.
