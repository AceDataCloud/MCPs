"""Shared helpers for Platform MCP tools."""

import json
from typing import Any

# Keys whose values grant account access or expose payment endpoints. Masked in
# read/list tool output; create/pay tools pass ``reveal=True`` so the caller gets
# the full freshly-minted token or the pay_url they need.
SECRET_KEYS = {"token", "password", "pay_id", "pay_url"}


def mask_secrets(obj: Any, reveal: bool = False) -> Any:
    """Recursively mask secret values unless ``reveal`` is True."""
    if reveal:
        return obj
    if isinstance(obj, dict):
        masked: dict[str, Any] = {}
        for key, value in obj.items():
            if key in SECRET_KEYS and isinstance(value, str) and value:
                masked[key] = f"{value[:10]}…({len(value)} chars)" if len(value) > 10 else "***"
            else:
                masked[key] = mask_secrets(value, reveal)
        return masked
    if isinstance(obj, list):
        return [mask_secrets(item, reveal) for item in obj]
    return obj


def dumps(obj: Any, reveal: bool = False) -> str:
    """Serialize a value to a pretty JSON string, masking secrets by default."""
    return json.dumps(mask_secrets(obj, reveal), ensure_ascii=False, indent=2)


def error_json(error: str, message: str) -> str:
    """Build a consistent error payload string."""
    return json.dumps({"error": error, "message": message}, ensure_ascii=False)


def confirmation_required(action: str, target: dict[str, Any]) -> str:
    """Build the dry-run preview returned when a write tool is called without confirm."""
    return json.dumps(
        {
            "status": "confirmation_required",
            "message": (
                "This is a write operation and was NOT executed. Review the target, "
                "then call again with confirm=true to proceed."
            ),
            "action": action,
            "target": target,
        },
        ensure_ascii=False,
        indent=2,
    )
