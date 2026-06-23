"""Configuration management for the AceDataCloud Docs MCP server."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

_env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)


@dataclass
class Settings:
    """Application settings loaded from environment variables.

    The docs server is PUBLIC — it only reads AceDataCloud's public, read-only
    endpoints, so no API token is required.
    """

    api_base_url: str = field(
        default_factory=lambda: os.getenv("ACEDATACLOUD_API_BASE_URL", "https://api.acedata.cloud")
    )
    platform_base_url: str = field(
        default_factory=lambda: os.getenv(
            "ACEDATACLOUD_PLATFORM_BASE_URL", "https://platform.acedata.cloud"
        )
    )
    request_timeout: float = field(
        default_factory=lambda: float(os.getenv("DOCS_REQUEST_TIMEOUT", "30"))
    )

    server_name: str = field(
        default_factory=lambda: os.getenv("MCP_SERVER_NAME", "AceDataCloud Docs")
    )
    transport: str = field(default_factory=lambda: os.getenv("MCP_TRANSPORT", "stdio"))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    # Set only if OAuth is ever desired; left empty → server stays public/no-auth.
    server_url: str = field(default_factory=lambda: os.getenv("MCP_SERVER_URL", ""))
    oauth_client_id: str = field(
        default_factory=lambda: os.getenv("ACEDATACLOUD_OAUTH_CLIENT_ID", "")
    )


settings = Settings()
