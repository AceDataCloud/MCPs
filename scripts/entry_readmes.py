"""Generate the first-use section shared by GitHub/PyPI and editor listings."""
from urllib.parse import urlencode

try:
    from .mcp_catalog import documentation_target, load_catalog
except ImportError:
    from mcp_catalog import documentation_target, load_catalog

ENTRIES = {
    "suno": ("SunoMCP", "a playable music track", "Generate an instrumental lo-fi track, then poll the task until it completes and return the final audio URL."),
    "midjourney": ("MidjourneyMCP", "a viewable image", "Generate an image of a ceramic cup on a sunny desk, then retrieve the completed task and final image URL."),
    "seedance": ("SeedanceMCP", "a playable video", "Generate a short video of clouds moving over a mountain, then retrieve the completed task and final video URL."),
}

def entry_url(alias, content="quick_start", medium="readme"):
    target, _ = documentation_target(load_catalog()[alias])
    if not target:
        raise ValueError(f"No active public target for {alias}")
    # A public entry must open independently of analytics availability.
    return target + "?" + urlencode({
        "utm_source": ENTRIES[alias][0].lower(),
        "utm_medium": medium, "utm_campaign": "opensource_activation", "utm_content": content,
    })

def render(alias):
    name, result, prompt = ENTRIES[alias]
    endpoint = f"https://{alias}.mcp.acedata.cloud/mcp"
    return f"""<!-- BEGIN GENERATED FIRST USE: scripts/build_entry_readmes.py -->
## Start with the hosted server

[Setup guide and pricing information]({entry_url(alias)}) · [Example prompt](#verify-your-first-result)

1. In a client that supports remote MCP OAuth, add **`{endpoint}`** as an HTTP server.
2. Choose **Connect / Sign in**, log in to AceDataCloud, review the requested permissions, and authorize.
3. Enable the tools and ask for {result}. You do not need to create or paste an API token for this route.

The server already supports OAuth discovery, dynamic client registration (DCR), and S256 PKCE.
DCR registers the **client application**; you still sign in and approve access. Authorization does
not make generation free. Review the consent screen: the media integration can read your profile
and manage the applications and credentials used for API access. Usage is charged to your account.

### Client compatibility

| Client / mode | Start path | Boundary |
| --- | --- | --- |
| Claude web / Desktop with remote custom connectors | Add the URL in the connector UI, then authorize | Availability and menu names depend on your plan and app version. The local Desktop JSON is for stdio; do not paste HTTP config there. |
| VS Code with native remote MCP support | Run **MCP: Add Server**, select HTTP, paste the URL, then follow authentication | Use a version with OAuth/DCR support. The optional AceDataCloud extension has its own API-key setup. |
| Other remote clients | Use the client's documented HTTP + OAuth flow | Support varies by client and version; an endpoint alone does not prove the client's login flow works. |
| Local stdio / self-hosted / clients without OAuth | Use the API Token path below | Keep the token in a local secret or environment variable; never in the server URL or Git. |

### Verify your first result

> {prompt}

This is a reproducible example prompt, not a promised generation time or a recorded success.
A connected server, `tools/list`, and a task ID only confirm setup/submission. Keep the task ID,
wait for terminal success, then open or play the final media. Pending previews and failed tasks
are not a completed result. [View setup and billing guidance]({entry_url(alias, 'usage')}).

### Charges and common failures

- The MCP code is open source; hosted API generation is metered. Check current service pricing,
  model availability, account balance, and applicable terms before generating. No free allowance
  or commercial-use right is implied by installing this package.
- **Login loop / 401:** reconnect using the client's authentication UI; for local usage check the
  token and its scope. Update a client that cannot discover or register an OAuth server.
- **403 / access denied:** inspect the error and account permissions; a moderation rejection
  requires changing the input. **Insufficient balance:** inspect billing before retrying.
- **Pending / failed generation:** poll the same task; read the final error. Do not repeatedly
  submit new tasks to fix polling. A new generation may incur a new charge.

### API Token path

For local stdio or a client without OAuth, [open the setup page]({entry_url(alias, 'api_token')}),
sign in, choose the service, and create an API credential with the required scope. Configure
`ACEDATACLOUD_API_TOKEN` locally, or use the client's documented Bearer-header setting.
Use the local commands below for stdio; HTTP configuration formats are client-specific.

The setup link opens the existing page directly and carries four campaign labels. Analytics
failures never block the page. Pasting
the bare endpoint directly into a native client remains supported; if no source can be matched,
that visit is reported as unknown. No token belongs in a tracking link.
<!-- END GENERATED FIRST USE -->

"""
