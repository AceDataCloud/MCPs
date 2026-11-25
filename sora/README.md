# SoraMCP (retired)

<!-- mcp-name: io.github.AceDataCloud/mcp-sora -->

The AceDataCloud Sora integration is retired. Its hosted MCP server and public
Sora API endpoints are no longer offered. Installing an older package does not
restore access to the retired service.

This directory retains historical source for existing integrations and reference.
Its tool definitions and examples describe the former API, not currently available
capabilities. Do not configure a new connection to `sora.mcp.acedata.cloud`.

For a supported video workflow, choose a currently published service such as
[Seedance](https://platform.acedata.cloud/documents/seedance-mcp),
[Veo](https://platform.acedata.cloud/documents/veo-mcp), or
[Kling](https://platform.acedata.cloud/documents/kling).
Check the selected service's current models, input requirements and pricing;
Sora prompts, character references, durations and task IDs are not interchangeable.

Historical tasks are not automatically migrated to another service. Preserve any
previously downloaded media and avoid resubmitting a retired task as a new generation.

## Historical source development

Offline compatibility tests can be run with `pytest -m "not integration"`.
No deployment or endpoint reactivation is included in this repository's retirement.

## License

MIT License — see [LICENSE](LICENSE).
