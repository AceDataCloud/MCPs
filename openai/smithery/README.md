# Connect to GPT Image directly

Smithery retired its managed connections and accounts on October 31, 2026. Its public directory remains available. [Platform announcement](https://smithery.ai/future)

Add `https://openai.mcp.acedata.cloud/mcp` as a Streamable HTTP server in your MCP client and follow the client's authorization prompt. Update existing connections that use a Smithery proxy URL to this Ace Data Cloud endpoint. See the [service setup guide](../README.md) for installation and application keys.

Check [current pricing and account access](https://platform.acedata.cloud/documents/openai?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen) before generating. To check progress, pass the original task's `id` to `openai_get_task`.
