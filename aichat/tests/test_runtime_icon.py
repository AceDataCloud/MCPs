"""Validate the icon actually advertised during MCP initialization."""

import pytest
from mcp.shared.memory import create_connected_server_and_client_session
from pydantic import AnyHttpUrl, TypeAdapter, ValidationError

import tools  # noqa: F401 - register the actual service tools
from core.server import mcp


@pytest.mark.asyncio
async def test_initialize_advertises_a_valid_public_png_icon_and_existing_tools():
    async with create_connected_server_and_client_session(mcp) as session:
        initialized = await session.initialize()
        listed = await session.list_tools()

    assert initialized.serverInfo.name == "aichat"
    assert initialized.serverInfo.icons is not None
    assert len(initialized.serverInfo.icons) == 1
    icon = initialized.serverInfo.icons[0]
    # SDK Icon.src is a plain string; a successful initialize alone does not
    # enforce the protocol schema's URI format. Reject the former empty value.
    url = TypeAdapter(AnyHttpUrl).validate_python(icon.src)
    assert url.scheme == "https"
    assert url.host == "raw.githubusercontent.com"
    assert url.path.endswith("/vscode-bundle/icon.png")
    assert icon.mimeType == "image/png"
    with pytest.raises(ValidationError):
        TypeAdapter(AnyHttpUrl).validate_python("")
    assert {tool.name for tool in listed.tools} == {
        "aichat_create_conversation",
        "aichat_create_conversation_v2",
        "aichat_list_models",
        "aichat_get_usage_guide",
    }
