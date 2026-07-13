"""Shared FastMCP server instance."""

import logging

from mcp.server.fastmcp import FastMCP

from core.config import settings

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

mcp_kwargs: dict = {"host": "0.0.0.0"}
oauth_provider = None

if settings.server_url:
    from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions, RevocationOptions
    from pydantic import AnyHttpUrl

    from core.oauth import AceDataCloudOAuthProvider

    oauth_provider = AceDataCloudOAuthProvider()
    mcp_kwargs["auth_server_provider"] = oauth_provider
    mcp_kwargs["auth"] = AuthSettings(
        issuer_url=AnyHttpUrl(settings.server_url),
        resource_server_url=AnyHttpUrl(settings.server_url),
        client_registration_options=ClientRegistrationOptions(
            enabled=True,
            valid_scopes=["mcp:access"],
            default_scopes=["mcp:access"],
        ),
        revocation_options=RevocationOptions(enabled=True),
        required_scopes=["mcp:access"],
    )

mcp = FastMCP(settings.server_name, **mcp_kwargs)
