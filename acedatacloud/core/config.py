"""Configuration management for the Platform MCP server."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

# Load .env file from project root
_env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    # Management API configuration. NOTE: this targets the platform console API
    # (platform.acedata.cloud), authenticated with a PLATFORM token — not the
    # per-service api.acedata.cloud data token.
    api_base_url: str = field(
        default_factory=lambda: os.getenv("PLATFORM_API_BASE_URL", "https://platform.acedata.cloud")
    )
    api_token: str = field(default_factory=lambda: os.getenv("ACEDATACLOUD_PLATFORM_TOKEN", ""))

    # Request configuration
    request_timeout: float = field(
        default_factory=lambda: float(os.getenv("PLATFORM_REQUEST_TIMEOUT", "30"))
    )

    # Server configuration
    server_name: str = field(default_factory=lambda: os.getenv("MCP_SERVER_NAME", "acedatacloud"))
    transport: str = field(default_factory=lambda: os.getenv("MCP_TRANSPORT", "stdio"))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    # OAuth / remote-auth configuration. When MCP_SERVER_URL is set, the HTTP
    # transport enables OAuth 2.1 (DCR) and delegates user login to
    # auth.acedata.cloud, then mints a durable, non-expiring platform-* token
    # (via platform.acedata.cloud) and issues it as the access token — so
    # redeploys/restarts never force re-authorization.
    server_url: str = field(default_factory=lambda: os.getenv("MCP_SERVER_URL", ""))
    auth_base_url: str = field(
        default_factory=lambda: os.getenv(
            "ACEDATACLOUD_AUTH_BASE_URL", "https://auth.acedata.cloud"
        )
    )
    oauth_client_id: str = field(
        default_factory=lambda: os.getenv("ACEDATACLOUD_OAUTH_CLIENT_ID", "")
    )

    def validate(self) -> None:
        """Validate required settings."""
        if not self.api_token:
            raise ValueError(
                "ACEDATACLOUD_PLATFORM_TOKEN environment variable is required. "
                "Create one at https://platform.acedata.cloud/console/platform-tokens"
            )

    @property
    def is_configured(self) -> bool:
        """Check if the platform token is configured."""
        return bool(self.api_token)


# Global settings instance
settings = Settings()
