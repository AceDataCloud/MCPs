"""Configuration management for MCP Discord Bot server."""

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

    # Discord Bot Configuration
    bot_base_url: str = field(default_factory=lambda: os.getenv("DISCORD_BOT_BASE_URL", ""))
    bot_token: str = field(default_factory=lambda: os.getenv("DISCORD_BOT_TOKEN", ""))

    # Request Configuration
    request_timeout: float = field(
        default_factory=lambda: float(os.getenv("DISCORD_BOT_REQUEST_TIMEOUT", "30"))
    )

    # Server Configuration
    server_name: str = field(default_factory=lambda: os.getenv("MCP_SERVER_NAME", "discord-bot"))
    transport: str = field(default_factory=lambda: os.getenv("MCP_TRANSPORT", "stdio"))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    def validate(self) -> None:
        """Validate required settings."""
        if not self.bot_base_url:
            raise ValueError(
                "DISCORD_BOT_BASE_URL environment variable is required. "
                "Deploy a Discord Agent Proxy on https://platform.acedata.cloud and set the URL."
            )
        if not self.bot_token:
            raise ValueError(
                "DISCORD_BOT_TOKEN environment variable is required. "
                "Get your token from the Discord Agent Proxy configuration page."
            )

    @property
    def is_configured(self) -> bool:
        """Check if the bot is configured."""
        return bool(self.bot_base_url and self.bot_token)


# Global settings instance
settings = Settings()
