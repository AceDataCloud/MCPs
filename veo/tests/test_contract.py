"""Guards against re-introducing models/params the API no longer accepts."""

from typing import get_args

import tools  # noqa: F401
from core.client import VeoClient
from core.server import mcp
from core.types import DEFAULT_MODEL, AspectRatio, VeoModel

# Mirrors the `model` / `aspect_ratio` enums in the Veo OpenAPI spec.
SPEC_MODELS = {"veo3", "veo3-fast", "veo31", "veo31-fast", "veo31-fast-ingredients"}
SPEC_ASPECT_RATIOS = {"16:9", "9:16"}
CURRENT_TOOLS = {
    "veo_get_1080p",
    "veo_get_prompt_guide",
    "veo_get_task",
    "veo_get_tasks_batch",
    "veo_image_to_video",
    "veo_list_actions",
    "veo_list_models",
    "veo_text_to_video",
}
RETIRED_TOOLS = {
    "veo_extend_video",
    "veo_reshoot",
    "veo_upsample",
    "veo_video_objects",
}


def test_models_match_spec():
    assert set(get_args(VeoModel)) == SPEC_MODELS


def test_retired_models_are_gone():
    # veo2/veo2-fast were retired upstream and now 400.
    assert "veo2" not in get_args(VeoModel)
    assert "veo2-fast" not in get_args(VeoModel)


def test_aspect_ratios_match_spec():
    assert set(get_args(AspectRatio)) == SPEC_ASPECT_RATIOS


def test_default_model_is_selectable():
    assert DEFAULT_MODEL in get_args(VeoModel)


def test_discovery_exposes_only_current_tools():
    discovered = {tool.name for tool in mcp._tool_manager.list_tools()}

    assert discovered == CURRENT_TOOLS
    assert discovered.isdisjoint(RETIRED_TOOLS)


def test_retired_tool_client_methods_remain_available():
    for method_name in ("upsample_video", "extend_video", "reshoot_video", "video_objects"):
        assert callable(getattr(VeoClient, method_name))
