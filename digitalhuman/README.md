# MCP Digital Human Server

A [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server for the
AceDataCloud Digital Human API.

## Features

- Create lip-synced digital human videos from a source face video or image
- Clone voices from short reference audio samples
- Poll, batch-retrieve, or delete Digital Human tasks

## Connect locally

Use the local stdio package and an AceDataCloud API token. The public hosted HTTPS endpoint could not be verified, so this README does not offer it as a connection option. The local MCP process still calls AceDataCloud's API; it does not run the underlying service offline.

<!-- BEGIN TOKEN ONBOARDING -->
1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=digitalhuman_mcp_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=digitalhuman_mcp_readme_models).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.
<!-- END TOKEN ONBOARDING -->


### Local stdio

Install the package and give the local process an API token:

```bash
python -m pip install mcp-digitalhuman
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
mcp-digitalhuman
```

For Claude Desktop local MCP, merge this entry into the file opened by its developer settings (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS). `uvx` requires [uv](https://docs.astral.sh/uv/) on `PATH`:

```json
{
  "mcpServers": {
    "digitalhuman": {
      "command": "uvx",
      "args": ["mcp-digitalhuman"],
      "env": {"ACEDATACLOUD_API_TOKEN": "YOUR_API_TOKEN"}
    }
  }
}
```

Keep this user-level file private. Self-hosted HTTP uses `mcp-digitalhuman --transport http --port 8000`; expose it only with suitable network and TLS controls. Local execution still calls the AceDataCloud API.

### Check the connection

Confirm that the MCP client loads its tools. For an existing task ID, `digitalhuman_get_task` makes an authenticated query; loading the tool alone does not prove downstream API access. A real service request can be billed. If it returns 401, check the API token; if it returns 403 or an account/balance error, read that response before retrying.

## Development

```bash
pip install -e ".[dev,test]"
pytest -q
ruff check .
```

## Documentation

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/digitalhuman?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=digitalhuman_mcp_readme_quick_start)
