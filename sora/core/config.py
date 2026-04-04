"""Configuration management for MCP Sora server."""

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

    # API Configuration
    api_base_url: str = field(
        default_factory=lambda: os.getenv("ACEDATACLOUD_API_BASE_URL", "https://api.acedata.cloud")
    )
    api_token: str = field(default_factory=lambda: os.getenv("ACEDATACLOUD_API_TOKEN", ""))

    # Default Model
    default_model: str = field(default_factory=lambda: os.getenv("SORA_DEFAULT_MODEL", "sora-2"))

    # Default Video Settings (version 1)
    default_size: str = field(default_factory=lambda: os.getenv("SORA_DEFAULT_SIZE", "large"))
    default_duration: int = field(
        default_factory=lambda: int(os.getenv("SORA_DEFAULT_DURATION", "15"))
    )
    default_orientation: str = field(
        default_factory=lambda: os.getenv("SORA_DEFAULT_ORIENTATION", "landscape")
    )

    # Default Video Settings (version 2)
    default_seconds: int = field(
        default_factory=lambda: int(os.getenv("SORA_DEFAULT_SECONDS", "4"))
    )
    default_resolution: str = field(
        default_factory=lambda: os.getenv("SORA_DEFAULT_RESOLUTION", "1280x720")
    )

    # Request Configuration
    request_timeout: float = field(
        default_factory=lambda: float(os.getenv("SORA_REQUEST_TIMEOUT", "3600"))
    )

    # Server Configuration
    server_name: str = field(default_factory=lambda: os.getenv("MCP_SERVER_NAME", "sora"))
    transport: str = field(default_factory=lambda: os.getenv("MCP_TRANSPORT", "stdio"))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    # OAuth / Remote Auth Configuration
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

    def validate(self) -> None:
        """Validate required settings."""
        if not self.api_token:
            raise ValueError(
                "ACEDATACLOUD_API_TOKEN environment variable is required."
                "Get your token from https://platform.acedata.cloud"
            )

    @property
    def is_configured(self) -> bool:
        """Check if the API token is configured."""
        return bool(self.api_token)


# Global settings instance
settings = Settings()
