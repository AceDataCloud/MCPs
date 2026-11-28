# MCP HCaptcha Server

A Model Context Protocol (MCP) server for AceDataCloud's hCaptcha captcha-solving APIs.

## Features
- Solve hCaptcha image challenges and retrieve hCaptcha site tokens.
- Shared async task polling via `/captcha/tasks`
- Bearer-token authentication through AceDataCloud

## Connect locally

Use the local stdio package and an AceDataCloud API token. The public hosted HTTPS endpoint could not be verified, so this README does not offer it as a connection option. The local MCP process still calls AceDataCloud's API; it does not run the underlying service offline.

<!-- BEGIN TOKEN ONBOARDING -->
Sign in to [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. If it is missing, select **Initialize General Application**. Click the copy button marked **1** beside **API KEY**.

![Copy the General Application API key with the button marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

Store the raw key in your client’s credential store or in the environment variable shown below. Add `Bearer ` only when setting an HTTP `Authorization` header yourself. Check access to the required operations, the current pricing, and the application balance. To use a separate key for this integration, open **Manage Keys** to set **Allowed APIs**, expiration, and usage limit.
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
[Service details](https://platform.acedata.cloud/services/018c653e-4f1b-433f-82f9-732ef2767040?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
