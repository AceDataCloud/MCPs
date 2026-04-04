"""Unit tests for configuration."""

import os
from unittest.mock import patch

import pytest


class TestSettings:
    """Tests for Settings class."""

    def test_default_settings(self):
        """Test default settings values."""
        with patch.dict(os.environ, {}, clear=True):
            from core.config import Settings

            settings = Settings()
            assert settings.api_base_url == "https://api.acedata.cloud"
            assert settings.default_model == "sora-2"
            assert settings.default_size == "large"
            assert settings.default_duration == 15
            assert settings.default_orientation == "landscape"
            assert settings.request_timeout == 3600
            assert settings.server_name == "sora"
            assert settings.transport == "stdio"
            assert settings.log_level == "INFO"

    def test_settings_from_env(self):
        """Test settings loaded from environment variables."""
        env_vars = {
            "ACEDATACLOUD_API_TOKEN": "test-token",
            "ACEDATACLOUD_API_BASE_URL": "https://custom.api.com",
            "SORA_DEFAULT_MODEL": "sora-2-pro",
            "SORA_DEFAULT_SIZE": "small",
            "SORA_DEFAULT_DURATION": "25",
            "SORA_DEFAULT_ORIENTATION": "portrait",
            "SORA_REQUEST_TIMEOUT": "600",
            "MCP_SERVER_NAME": "custom-sora",
            "LOG_LEVEL": "DEBUG",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            from core.config import Settings

            settings = Settings()
            assert settings.api_token == "test-token"
            assert settings.api_base_url == "https://custom.api.com"
            assert settings.default_model == "sora-2-pro"
            assert settings.default_size == "small"
            assert settings.default_duration == 25
            assert settings.default_orientation == "portrait"
            assert settings.request_timeout == 600
            assert settings.server_name == "custom-sora"
            assert settings.log_level == "DEBUG"

    def test_is_configured(self):
        """Test is_configured property."""
        with patch.dict(os.environ, {"ACEDATACLOUD_API_TOKEN": "test-token"}, clear=True):
            from core.config import Settings

            settings = Settings()
            assert settings.is_configured is True

        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.is_configured is False

    def test_validate_missing_token(self):
        """Test validate raises error when token is missing."""
        with patch.dict(os.environ, {}, clear=True):
            from core.config import Settings

            settings = Settings()
            with pytest.raises(ValueError, match="ACEDATACLOUD_API_TOKEN"):
                settings.validate()
