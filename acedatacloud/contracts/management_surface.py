"""Generated, fixed-route management tools and backend coverage ledger."""

import json
from pathlib import Path
from typing import Any

SURFACE: dict[str, Any] = json.loads(Path(__file__).with_suffix(".json").read_text())
SURFACE_TOOLS: list[dict[str, Any]] = SURFACE["tools"]
BACKEND_OPERATIONS: list[dict[str, Any]] = SURFACE["operations"]
