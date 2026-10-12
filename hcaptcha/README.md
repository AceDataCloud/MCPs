# MCP HCaptcha Server

A Model Context Protocol (MCP) server for AceDataCloud's hCaptcha captcha-solving APIs.

## Features
- Solve hCaptcha image challenges and retrieve hCaptcha site tokens.
- Shared async task polling via `/captcha/tasks`
- Bearer-token authentication through AceDataCloud

## Connect locally

Use the local stdio package and an AceDataCloud API token. The public hosted HTTPS endpoint could not be verified, so this README does not offer it as a connection option. The local MCP process still calls AceDataCloud's API; it does not run the underlying service offline.

<!-- BEGIN TOKEN ONBOARDING -->
1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=hcaptcha_mcp_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=hcaptcha_mcp_readme_models).
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
python -m pip install mcp-hcaptcha
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
mcp-hcaptcha
```

For Claude Desktop local MCP, merge this entry into the file opened by its developer settings (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS). `uvx` requires [uv](https://docs.astral.sh/uv/) on `PATH`:

```json
{
  "mcpServers": {
    "hcaptcha": {
      "command": "uvx",
      "args": ["mcp-hcaptcha"],
      "env": {"ACEDATACLOUD_API_TOKEN": "YOUR_API_TOKEN"}
    }
  }
}
```

Keep this user-level file private. Self-hosted HTTP uses `mcp-hcaptcha --transport http --port 8000`; expose it only with suitable network and TLS controls. Local execution still calls the AceDataCloud API.

### Check the connection

Confirm that the MCP client loads its tools. `hcaptcha_get_usage_guide` returns reference information; it does not prove downstream API access or balance. A real service request can be billed. If it returns 401, check the API token; if it returns 403 or an account/balance error, read that response before retrying.

## Tools
- `hcaptcha_recognize` — Recognize hCaptcha image challenges
- `hcaptcha_get_token` — Get an hCaptcha token for a website, optionally with `rqdata`
- `hcaptcha_get_task` — Poll a captcha task result
- `hcaptcha_get_usage_guide` — Get hCaptcha usage guide
- `hcaptcha_get_api_info` — Get hCaptcha API information

## Service details

<!-- canonical-documentation -->
[Service details](https://platform.acedata.cloud/services/018c653e-4f1b-433f-82f9-732ef2767040?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=hcaptcha_mcp_readme_quick_start)
