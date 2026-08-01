"""Environment-backed settings for the Digital Human MCP server."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")


@dataclass
class Settings:
    """Runtime configuration for the Digital Human MCP server."""

    api_base_url: str = field(
        default_factory=lambda: os.getenv("ACEDATACLOUD_API_BASE_URL", "https://api.acedata.cloud")
    )
    api_token: str = field(default_factory=lambda: os.getenv("ACEDATACLOUD_API_TOKEN", ""))
    request_timeout: float = field(
        default_factory=lambda: float(os.getenv("DIGITALHUMAN_REQUEST_TIMEOUT", "180"))
    )
    server_name: str = field(default_factory=lambda: os.getenv("MCP_SERVER_NAME", "digitalhuman"))
    transport: str = field(default_factory=lambda: os.getenv("MCP_TRANSPORT", "stdio"))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    server_url: str = field(default_factory=lambda: os.getenv("MCP_SERVER_URL", ""))
    auth_base_url: str = field(
        default_factory=lambda: os.getenv(
            "ACEDATACLOUD_AUTH_BASE_URL", "https://auth.acedata.cloud"
        )
    )
    platform_base_url: str = field(
        default_factory=lambda: os.getenv(
            "ACEDATACLOUD_PLATFORM_BASE_URL", "https://platform.acedata.cloud"
        )
    )
    oauth_client_id: str = field(
        default_factory=lambda: os.getenv("ACEDATACLOUD_OAUTH_CLIENT_ID", "")
    )

    @property
    def is_configured(self) -> bool:
        """Return whether a default API token is available."""
        return bool(self.api_token)


settings = Settings()
