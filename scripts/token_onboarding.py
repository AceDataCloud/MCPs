"""Shared credential instructions for generated MCP distribution READMEs."""

import html
import re

API_GUIDE = """Sign in to [Applications](https://platform.acedata.cloud/console/applications) and open **General Application**. If it is missing, select **Initialize General Application**. Click the copy button marked **1** beside **API KEY**.

![Copy the General Application API key with the button marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

Store the raw key in your client’s credential store or in the environment variable shown below. Add `Bearer ` only when setting an HTTP `Authorization` header yourself. Check access to the required operations, the current pricing, and the application balance. To use a separate key for this integration, open **Manage Keys** to set **Allowed APIs**, expiration, and usage limit.
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
