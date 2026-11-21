# Connect ACE Music in Cherry Studio

[Import into Cherry Studio](cherrystudio://mcp/install?servers=eyJuYW1lIjoiQUNFIE11c2ljIGJ5IEFjZSBEYXRhIENsb3VkIiwidHlwZSI6InN0cmVhbWFibGVIdHRwIiwiYmFzZVVybCI6Imh0dHBzOi8vYWNlbXVzaWMubWNwLmFjZWRhdGEuY2xvdWQvbWNwIiwiaGVhZGVycyI6e319) · [Inspect the credential-free JSON](cherry-studio.json)

In MCP Servers, add a Streamable HTTP server named ACE Music with URL `https://acemusic.mcp.acedata.cloud/mcp`. Configure a private Authorization header with a Bearer application key, or use the client's sign-in flow if offered. For a local stdio server use command `uvx` and argument `mcp-acemusic`, and set `ACEDATACLOUD_API_TOKEN` in its private environment.

Enable the server for the intended assistant, list tools, and call `acemusic_list_models`. To check an existing task, call `acemusic_get_task` with its original ID. [Application keys](https://platform.acedata.cloud/console/applications) · [Server card](https://acemusic.mcp.acedata.cloud/.well-known/mcp/server-card.json)
