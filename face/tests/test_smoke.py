"""Smoke tests for the Face Transform MCP server."""

import os
from unittest.mock import patch


def test_settings_defaults():
    """Settings load with sensible defaults."""
    from core.config import Settings

    with patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        assert settings.api_base_url == "https://api.acedata.cloud"
        assert settings.api_token == ""
        assert settings.server_name == "face"


def test_settings_token_from_env():
    """Settings pick up ACEDATACLOUD_API_TOKEN."""
    from core.config import Settings

    with patch.dict(os.environ, {"ACEDATACLOUD_API_TOKEN": "test-token"}, clear=True):
        settings = Settings()
        assert settings.api_token == "test-token"
        assert settings.is_configured is True


def test_server_module_loads():
    """The MCP server module loads without errors."""
    from core.server import mcp

    assert mcp is not None


def test_face_tools_register():
    """All face tools register on the FastMCP server."""
    import tools  # noqa: F401
    from core.server import mcp

    # FastMCP keeps registered tools on the internal tool manager.
    expected = {
        "face_detect_keypoints",
        "face_beautify",
        "face_change_age",
        "face_change_gender",
        "face_swap",
        "face_cartoonize",
        "face_detect_liveness",
        "face_get_usage_guide",
    }
    registered = {t.name for t in mcp._tool_manager.list_tools()}
    missing = expected - registered
    assert not missing, f"Missing tools: {missing}"


def test_face_prompts_register():
    """Both face prompts register on the FastMCP server."""
    import prompts  # noqa: F401
    from core.server import mcp

    expected = {"face_guide", "face_workflow_examples"}
    registered = {p.name for p in mcp._prompt_manager.list_prompts()}
    missing = expected - registered
    assert not missing, f"Missing prompts: {missing}"
