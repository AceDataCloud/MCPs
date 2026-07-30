"""Configuration management for MCP HCaptcha server."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

_env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    api_base_url: str = field(default_factory=lambda: os.getenv("ACEDATACLOUD_API_BASE_URL", "https://api.acedata.cloud"))
    api_token: str = field(default_factory=lambda: os.getenv("ACEDATACLOUD_API_TOKEN", ""))
    request_timeout: float = field(default_factory=lambda: float(os.getenv("HCAPTCHA_REQUEST_TIMEOUT", "120")))
    server_name: str = field(default_factory=lambda: os.getenv("MCP_SERVER_NAME", "hcaptcha"))
    transport: str = field(default_factory=lambda: os.getenv("MCP_TRANSPORT", "stdio"))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    server_url: str = field(default_factory=lambda: os.getenv("MCP_SERVER_URL", ""))
    auth_base_url: str = field(default_factory=lambda: os.getenv("ACEDATACLOUD_AUTH_BASE_URL", "https://auth.acedata.cloud"))
    platform_base_url: str = field(default_factory=lambda: os.getenv("ACEDATACLOUD_PLATFORM_BASE_URL", "https://platform.acedata.cloud"))
    oauth_client_id: str = field(default_factory=lambda: os.getenv("ACEDATACLOUD_OAUTH_CLIENT_ID", ""))

    def validate(self) -> None:
        if not self.api_token:
            raise ValueError("ACEDATACLOUD_API_TOKEN environment variable is required. Get your token from https://platform.acedata.cloud")

    @property
    def is_configured(self) -> bool:
        return bool(self.api_token)


settings = Settings()
