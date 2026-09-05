# MCP Fish Server

<!-- mcp-name: io.github.AceDataCloud/mcp-fish -->

A Model Context Protocol (MCP) server for Fish Audio TTS (Text-to-Speech) via the AceDataCloud platform.
Generate natural-sounding speech and explore the Fish voice model library.

## Features

- **High-quality TTS**: Generate speech from text via Fish Audio models
- **Voice library**: Browse, search, and fetch metadata for Fish voice models
- **Asynchronous tasks**: Submit generation tasks and poll for results
- **Batch task lookup**: Query multiple task results in one call

### One-shot voice cloning

Pass one public HTTPS reference audio URL plus its exact transcript. This conditions only the current TTS request and does not create a reusable voice model:

```python
fish_generate_audio(
    text="New speech in the referenced voice",
    reference_audio_url="https://cdn.acedata.cloud/reference.mp3",
    reference_text="The exact words spoken in the reference audio",
)
```

Use `reference_id` for saved or public voices, and the one-shot reference fields for a temporary voice. Do not combine them. Reference audio supports MP3/WAV and should be 10–270 seconds. Billing remains based on the target text's UTF-8 byte count.

## Installation

```bash
pip install mcp-fish
```

## Configuration

Set your AceDataCloud API token:

```bash
export ACEDATACLOUD_API_TOKEN=your_token_here
```

Get your token from [https://platform.acedata.cloud](https://platform.acedata.cloud).

## Usage

### stdio mode (default)

```bash
mcp-fish
```

### HTTP mode

```bash
mcp-fish --transport http --port 8000
```

## Tool Reference

| Tool | Description |
|------|-------------|
| `fish_generate_audio` | Generate speech from text via a Fish voice model |
| `fish_list_models` | List available Fish voice models |
| `fish_get_model` | Fetch metadata for a specific Fish voice model |
| `fish_get_task` | Get the status / result of a generation task |
| `fish_get_tasks_batch` | Batch-fetch the status / result of multiple tasks |
| `fish_get_usage_guide` | Get the API usage guide |

## Documentation

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/fish)

## License

MIT — see [LICENSE](../LICENSE) at the repository root.
