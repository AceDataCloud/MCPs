"""Informational tools for the Platform MCP server."""

from contracts.render import render_usage_guide
from core.client import get_request_subject
from core.exceptions import PlatformError
from core.server import mcp
from core.utils import dumps, error_json


@mcp.tool()
async def acedatacloud_get_user_info() -> str:
    """Get the current authenticated AceDataCloud account's user profile.

    Returns id, username, email, nickname, and avatar for the account
    represented by the current platform credential. Useful for constructing
    personalized content (e.g. inviter_id referral links).
    """
    try:
        return dumps(await get_request_subject())
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_get_usage_guide() -> str:
    """Get a guide for using the AceDataCloud platform management tools.

    Explains the available tools, the write-confirmation model, and the
    authentication requirements.
    """
    return render_usage_guide()
