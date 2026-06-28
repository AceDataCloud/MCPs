"""Unit tests for configuration."""

from core.config import Settings


def test_defaults():
    s = Settings()
    assert s.api_base_url == "https://platform.acedata.cloud"
    assert s.server_name == "acedatacloud"
    assert s.request_timeout == 30.0


def test_is_configured_true():
    s = Settings(api_token="platform-v1-x")
    assert s.is_configured is True
    s.validate()  # should not raise


def test_is_configured_false_and_validate_raises():
    s = Settings(api_token="")
    assert s.is_configured is False
    try:
        s.validate()
        raise AssertionError("validate() should have raised")
    except ValueError as e:
        assert "ACEDATACLOUD_PLATFORM_TOKEN" in str(e)
