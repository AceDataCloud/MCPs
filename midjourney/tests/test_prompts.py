"""Tests for Midjourney MCP guidance prompts."""

from typing import get_type_hints

from core.types import DEFAULT_VERSION
from prompts import midjourney_image_generation_guide, midjourney_workflow_examples
from tools.imagine_tools import midjourney_imagine


def test_v81_guidance_excludes_unsupported_quality_and_turbo() -> None:
    guide = midjourney_image_generation_guide()
    examples = midjourney_workflow_examples()

    assert "Quality is unsupported" in guide
    assert "Turbo is not supported in V8.1" in guide
    assert "separate resolution-based rates" in guide
    assert "do not set `quality` or use Turbo" in examples
    assert "V8.1 only. Costs 4x credits" not in guide
    assert "HD+Q4 together cost 16x" not in examples


def test_v81_tool_schema_describes_supported_controls() -> None:
    hints = get_type_hints(midjourney_imagine, include_extras=True)
    descriptions = {name: hint.__metadata__[0].description for name, hint in hints.items() if hasattr(hint, "__metadata__")}

    assert "V8.1 only supports fast and relax" in descriptions["mode"]
    assert "separate SD and HD resolution-based rates" in descriptions["hd"]
    assert "not supported in V8.1" in descriptions["quality"]
    assert "selected SD/HD resolution rate" in descriptions["style_reference"]
    assert "selected SD/HD resolution rate" in descriptions["moodboard"]
    assert DEFAULT_VERSION == "8.1"
