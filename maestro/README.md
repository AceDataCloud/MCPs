# Maestro MCP Server

Produce complete videos from a natural-language brief with [Maestro](https://studio.acedata.cloud/maestro) through the Ace Data Cloud API. Maestro plans the script, creates or sources media, generates voiceover and music, edits, captions, renders, and returns finished video variants.

## Install

```bash
pip install mcp-maestro
export ACEDATACLOUD_API_TOKEN="your-token"
mcp-maestro
```

Get an API token from [platform.acedata.cloud](https://platform.acedata.cloud/console/applications).

For a hosted connection, use `https://maestro.mcp.acedata.cloud/mcp`. It accepts a direct Ace Data Cloud Bearer token and supports OAuth sign-in.

## Tools

| Tool | Purpose |
|---|---|
| `maestro_create_video` | Create a video or run `remix`, `edit`, or `extend` on an earlier task |
| `maestro_get_task` | Read progress, status, and final language variants for one task |
| `maestro_list_tasks` | List recent tasks for the authenticated account |

## Example

Ask an MCP client:

> Create a 45-second 16:9 English product launch video from this product photo. Use a premium editorial style and a documentary voice.

The tool returns a `task_id` immediately. Query that ID until `status` is `succeeded` or `failed`. Successful tasks expose videos in `response.data.variants`.

To revise an existing result, call `maestro_create_video` with an iteration action and the prior task ID:

```json
{
  "prompt": "Keep the visuals but tighten the first 10 seconds and use a warmer voice.",
  "action": "edit",
  "ref_task_id": "previous-task-id"
}
```

## MCP Client Configuration

```json
{
  "mcpServers": {
    "maestro": {
      "command": "uvx",
      "args": ["mcp-maestro"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your-token"
      }
    }
  }
}
```

## Development

```bash
pip install -e ".[dev,test,release]"
pytest --cov=core --cov=tools
ruff check .
ruff format --check .
mypy core tools main.py
python -m build
```

See the [Maestro API documentation](https://platform.acedata.cloud/documents/maestro) for billing and response details.