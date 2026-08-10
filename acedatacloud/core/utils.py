"""Shared helpers for Platform MCP tools."""

import json
from typing import Any

SECRET_KEYS = {
    "access_token",
    "api_key",
    "authorization",
    "client_secret",
    "delegation_tx",
    "file_key",
    "headers",
    "identity_token",
    "password",
    "pay_id",
    "pay_url",
    "private_key",
    "refresh_token",
    "revoked_tx",
    "secret",
    "setup_token",
    "setup_tx",
    "signature",
    "token",
}
SECRET_SUFFIXES = ("_api_key", "_password", "_private_key", "_secret", "_signature", "_token")


def mask_secrets(
    obj: Any,
    *,
    disclose: set[str] | None = None,
    path: str = "",
    reveal: bool = False,
) -> Any:
    """Recursively mask secret values except explicitly disclosed JSON paths.

    ``reveal`` remains for backward compatibility. New call sites must use
    ``disclose`` so one required secret cannot expose sibling fields.
    """
    if reveal:
        return obj
    disclosed = disclose or set()
    if isinstance(obj, dict):
        masked: dict[str, Any] = {}
        for key, value in obj.items():
            child_path = f"{path}/{_escape_pointer(key)}"
            if child_path in disclosed:
                masked[key] = value
            elif _is_secret_key(key):
                masked[key] = _masked_value(value)
            else:
                masked[key] = mask_secrets(value, disclose=disclosed, path=child_path)
        return masked
    if isinstance(obj, list):
        return [
            mask_secrets(value, disclose=disclosed, path=f"{path}/{index}")
            for index, value in enumerate(obj)
        ]
    return obj


def dumps(
    obj: Any,
    *,
    disclose: set[str] | None = None,
    reveal: bool = False,
) -> str:
    """Serialize JSON with recursive secret masking."""
    return json.dumps(
        mask_secrets(obj, disclose=disclose, reveal=reveal),
        ensure_ascii=False,
        indent=2,
    )


def error_json(error: str, message: str) -> str:
    """Build a consistent error payload string."""
    return json.dumps({"error": error, "message": message}, ensure_ascii=False)


def confirmation_required(action: str, target: dict[str, Any]) -> str:
    """Build a redacted dry-run preview for a write tool."""
    return json.dumps(
        {
            "status": "confirmation_required",
            "message": (
                "This is a write operation and was NOT executed. Review the target, "
                "then call again with confirm=true to proceed."
            ),
            "action": action,
            "target": mask_secrets(target),
        },
        ensure_ascii=False,
        indent=2,
    )


def _is_secret_key(key: str) -> bool:
    normalized = key.lower()
    return normalized in SECRET_KEYS or normalized.endswith(SECRET_SUFFIXES)


def _masked_value(value: Any) -> Any:
    if value is None or value == "":
        return value
    if isinstance(value, str):
        return f"{value[:4]}…({len(value)} chars)" if len(value) > 8 else "***"
    if isinstance(value, dict | list):
        return "***"
    return "***"


def _escape_pointer(value: str) -> str:
    return str(value).replace("~", "~0").replace("/", "~1")
