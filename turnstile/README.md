# MCP Turnstile Server

A Model Context Protocol (MCP) server for AceDataCloud's Turnstile captcha-solving APIs.

## Features
- Obtain Cloudflare Turnstile tokens.
- Bearer-token authentication through AceDataCloud

## Connect locally

Use the local stdio package and an AceDataCloud API token. The public hosted HTTPS endpoint could not be verified, so this README does not offer it as a connection option. The local MCP process still calls AceDataCloud's API; it does not run the underlying service offline.

Get an API credential through [AceDataCloud Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=turnstile_mcp_readme_platform), keep it out of committed files, and review current pricing before a billable call.

### Local stdio

Install the package and give the local process an API token:

```bash
python -m pip install mcp-turnstile
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
mcp-turnstile
```

For Claude Desktop local MCP, merge this entry into the file opened by its developer settings (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS). `uvx` requires [uv](https://docs.astral.sh/uv/) on `PATH`:

```json
{
  "mcpServers": {
    "turnstile": {
      "command": "uvx",
      "args": ["mcp-turnstile"],
      "env": {"ACEDATACLOUD_API_TOKEN": "YOUR_API_TOKEN"}
    }
  }
}
```

Keep this user-level file private. Self-hosted HTTP uses `mcp-turnstile --transport http --port 8000`; expose it only with suitable network and TLS controls. Local execution still calls the AceDataCloud API.

### Check the connection

Confirm that the MCP client loads its tools. `turnstile_get_usage_guide` returns reference information; it does not prove downstream API access or balance. A real service request can be billed. If it returns 401, check the API token; if it returns 403 or an account/balance error, read that response before retrying.

## Tools
- `turnstile_get_token` — Get a Cloudflare Turnstile token
- `turnstile_get_usage_guide` — Get Turnstile usage guide
- `turnstile_get_api_info` — Get Turnstile API information

## Documentation

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/turnstile?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=turnstile_mcp_readme_quick_start)
