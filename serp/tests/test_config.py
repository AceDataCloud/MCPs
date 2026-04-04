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
            assert settings.api_base_url == "https://api.acedata.cloud"
            assert settings.api_token == ""
            assert settings.request_timeout == 30.0
            assert settings.server_name == "serp"
            assert settings.transport == "stdio"
            assert settings.log_level == "INFO"

    def test_custom_values(self):
        """Test settings with custom environment variables."""
        env = {
            "ACEDATACLOUD_API_BASE_URL": "https://custom.api.com",
            "ACEDATACLOUD_API_TOKEN": "my-test-token",
            "SERP_REQUEST_TIMEOUT": "60",
            "MCP_SERVER_NAME": "custom-serp",
            "MCP_TRANSPORT": "http",
            "LOG_LEVEL": "DEBUG",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = Settings()
            assert settings.api_base_url == "https://custom.api.com"
            assert settings.api_token == "my-test-token"
            assert settings.request_timeout == 60.0
            assert settings.server_name == "custom-serp"
            assert settings.transport == "http"
            assert settings.log_level == "DEBUG"

    def test_is_configured_true(self):
        """Test is_configured returns True when token is set."""
        with patch.dict(os.environ, {"ACEDATACLOUD_API_TOKEN": "test-token"}, clear=True):
            settings = Settings()
            assert settings.is_configured is True

    def test_is_configured_false(self):
        """Test is_configured returns False when token is empty."""
        with patch.dict(os.environ, {"ACEDATACLOUD_API_TOKEN": ""}, clear=True):
            settings = Settings()
            assert settings.is_configured is False

    def test_validate_success(self):
        """Test validate passes with token configured."""
        with patch.dict(os.environ, {"ACEDATACLOUD_API_TOKEN": "test-token"}, clear=True):
            settings = Settings()
            # Should not raise
            settings.validate()

    def test_validate_failure(self):
        """Test validate raises error when token missing."""
        with patch.dict(os.environ, {"ACEDATACLOUD_API_TOKEN": ""}, clear=True):
            settings = Settings()
            with pytest.raises(ValueError, match="ACEDATACLOUD_API_TOKEN"):
                settings.validate()
