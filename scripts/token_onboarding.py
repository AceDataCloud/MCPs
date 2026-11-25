"""Shared credential instructions for generated MCP distribution READMEs."""

import html
import re

API_GUIDE = """1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.
"""

ACCOUNT_GUIDE = """1. Sign in or register at [Ace Data Cloud → Account Tokens](https://platform.acedata.cloud/console/platform-tokens).
2. Click **Create** and copy the token with the copy button. It starts with `platform-`; it is an account-management credential, separate from an application's generation API key.
3. Paste only the token into this account MCP's credential field, or set `ACEDATACLOUD_PLATFORM_TOKEN` for local stdio. Add `Bearer ` only when configuring an HTTP `Authorization` header yourself.
4. Keep it private and remove it from **Account Tokens** to revoke access when no longer needed. For a client that supports hosted OAuth, you can instead use the browser sign-in flow described in this guide.
"""


def token_guide(alias):
    return ACCOUNT_GUIDE if alias == "acedatacloud" else API_GUIDE


def token_guide_html(alias, format_url):
    """Render the controlled shared guide for JetBrains' HTML description."""

    def inline(text):
        text = html.escape(text)
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
        return re.sub(
            r"\[([^\]]+)\]\((https://[^)]+)\)",
            lambda m: (
                '<a href="'
                + html.escape(format_url(html.unescape(m[2])), quote=True)
                + '">'
                + m[1]
                + "</a>"
            ),
            text,
        )

    output = []
    for paragraph in token_guide(alias).strip().split("\n\n"):
        lines = paragraph.splitlines()
        if all(re.match(r"^\d+\. ", line) for line in lines):
            output.append(
                "<ol>"
                + "".join(
                    "<li>" + inline(re.sub(r"^\d+\. ", "", line)) + "</li>"
                    for line in lines
                )
                + "</ol>"
            )
        elif image := re.fullmatch(r"!\[([^\]]+)\]\((https://[^)]+)\)", paragraph):
            output.append(
                '<p><img alt="'
                + html.escape(image[1], quote=True)
                + '" src="'
                + html.escape(image[2], quote=True)
                + '" /></p>'
            )
        else:
            output.append("<p>" + inline(paragraph) + "</p>")
    return "\n".join(output)


def refresh_token_guide(text, alias):
    return re.sub(
        r"(?s)<!-- BEGIN TOKEN ONBOARDING -->.*?<!-- END TOKEN ONBOARDING -->",
        lambda _: (
            "<!-- BEGIN TOKEN ONBOARDING -->\n"
            + token_guide(alias)
            + "<!-- END TOKEN ONBOARDING -->"
        ),
        text,
    )
