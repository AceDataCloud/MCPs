"""Unit tests for configuration."""

import os
from unittest.mock import patch

import pytest

from core.config import Settings


class TestSettings:
    """Tests for Settings configuration class."""

    def test_default_values(self):
        """Test default settings values."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.api_base_url == "https://api.acedata.cloud"
            assert settings.api_token == ""
            assert settings.request_timeout == 60.0
            assert settings.server_name == "aichat"
            assert settings.log_level == "INFO"

    def test_custom_values_from_env(self):
        """Test settings loaded from environment variables."""
        with patch.dict(
            os.environ,
            {
                "ACEDATACLOUD_API_TOKEN": "test-token-123",
                "ACEDATACLOUD_API_BASE_URL": "https://custom.api.com",
                "AICHAT_REQUEST_TIMEOUT": "120",
                "LOG_LEVEL": "DEBUG",
            },
        ):
            settings = Settings()
            assert settings.api_token == "test-token-123"
            assert settings.api_base_url == "https://custom.api.com"
            assert settings.request_timeout == 120.0
            assert settings.log_level == "DEBUG"

    def test_is_configured_with_token(self):
        """Test is_configured returns True when token is set."""
        with patch.dict(os.environ, {"ACEDATACLOUD_API_TOKEN": "my-token"}):
            settings = Settings()
            assert settings.is_configured is True

    def test_is_configured_without_token(self):
        """Test is_configured returns False when token is not set."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.is_configured is False

    def test_validate_raises_without_token(self):
        """Test validate raises ValueError when token is missing."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            with pytest.raises(ValueError, match="ACEDATACLOUD_API_TOKEN"):
                settings.validate()

    def test_validate_passes_with_token(self):
        """Test validate passes when token is set."""
        with patch.dict(os.environ, {"ACEDATACLOUD_API_TOKEN": "valid-token"}):
            settings = Settings()
            settings.validate()  # Should not raise
