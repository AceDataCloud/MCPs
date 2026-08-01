"""Unit tests for configuration module."""

import os
from unittest.mock import patch

import pytest

from core.config import Settings


class TestSettings:
    """Tests for Settings class."""

    def test_default_values(self):
        """Test default settings values."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.bot_base_url == ""
            assert settings.bot_token == ""
            assert settings.request_timeout == 30.0
            assert settings.server_name == "discord-bot"
            assert settings.transport == "stdio"
            assert settings.log_level == "INFO"

    def test_custom_values(self):
        """Test settings with custom environment variables."""
        env = {
            "DISCORD_BOT_BASE_URL": "https://discord-bot-test.app.acedata.cloud",
            "DISCORD_BOT_TOKEN": "my-test-token",
            "DISCORD_BOT_REQUEST_TIMEOUT": "60",
            "MCP_SERVER_NAME": "custom-discord",
            "MCP_TRANSPORT": "http",
            "LOG_LEVEL": "DEBUG",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = Settings()
            assert settings.bot_base_url == "https://discord-bot-test.app.acedata.cloud"
            assert settings.bot_token == "my-test-token"
            assert settings.request_timeout == 60.0
            assert settings.server_name == "custom-discord"
            assert settings.transport == "http"
            assert settings.log_level == "DEBUG"

    def test_is_configured_true(self):
        """Test is_configured returns True when both URL and token are set."""
        env = {
            "DISCORD_BOT_BASE_URL": "https://discord-bot-test.app.acedata.cloud",
            "DISCORD_BOT_TOKEN": "test-token",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = Settings()
            assert settings.is_configured is True

    def test_is_configured_false_no_url(self):
        """Test is_configured returns False when URL is missing."""
        with patch.dict(os.environ, {"DISCORD_BOT_TOKEN": "test-token"}, clear=True):
            settings = Settings()
            assert settings.is_configured is False

    def test_is_configured_false_no_token(self):
        """Test is_configured returns False when token is missing."""
        env = {"DISCORD_BOT_BASE_URL": "https://discord-bot-test.app.acedata.cloud"}
        with patch.dict(os.environ, env, clear=True):
            settings = Settings()
            assert settings.is_configured is False

    def test_validate_success(self):
        """Test validate passes when both URL and token are configured."""
        env = {
            "DISCORD_BOT_BASE_URL": "https://discord-bot-test.app.acedata.cloud",
            "DISCORD_BOT_TOKEN": "test-token",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = Settings()
            # Should not raise
            settings.validate()

    def test_validate_failure_no_url(self):
        """Test validate raises error when URL is missing."""
        with patch.dict(os.environ, {"DISCORD_BOT_TOKEN": "test-token"}, clear=True):
            settings = Settings()
            with pytest.raises(ValueError, match="DISCORD_BOT_BASE_URL"):
                settings.validate()

    def test_validate_failure_no_token(self):
        """Test validate raises error when token is missing."""
        env = {"DISCORD_BOT_BASE_URL": "https://discord-bot-test.app.acedata.cloud"}
        with patch.dict(os.environ, env, clear=True):
            settings = Settings()
            with pytest.raises(ValueError, match="DISCORD_BOT_TOKEN"):
                settings.validate()
