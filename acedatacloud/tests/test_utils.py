"""Unit tests for the utility helpers."""

import json

from core.utils import confirmation_required, dumps, error_json, mask_secrets


def test_mask_secrets_masks_token():
    data = {"token": "abcdef0123456789", "name": "ci"}
    masked = mask_secrets(data)
    assert masked["token"].endswith("chars)")
    assert "abcdef0123456789" not in masked["token"]
    assert masked["name"] == "ci"


def test_mask_secrets_masks_known_keys_suffixes_and_nested_values():
    data = {
        "api_key": "supplier-secret",
        "custom_private_key": "private-material",
        "headers": {"Authorization": "Bearer secret"},
        "items": [{"client_secret": "client-secret", "ok": 1}],
    }
    masked = mask_secrets(data)
    serialized = json.dumps(masked)
    for secret in ("supplier-secret", "private-material", "Bearer secret", "client-secret"):
        assert secret not in serialized
    assert masked["items"][0]["ok"] == 1


def test_mask_secrets_short_value():
    assert mask_secrets({"password": "abc"})["password"] == "***"


def test_mask_secrets_reveal_passthrough_is_backward_compatible():
    data = {"token": "abcdef0123456789"}
    assert mask_secrets(data, reveal=True) == data


def test_dumps_discloses_only_exact_json_pointer():
    out = json.loads(
        dumps(
            {
                "token": "new-token",
                "nested": {"token": "sibling-token"},
                "api_key": "provider-key",
            },
            disclose={"/token"},
        )
    )
    assert out["token"] == "new-token"
    assert out["nested"]["token"] != "sibling-token"
    assert out["api_key"] != "provider-key"


def test_dumps_escapes_json_pointer_keys():
    out = json.loads(dumps({"a/b": {"token": "value"}}, disclose={"/a~1b/token"}))
    assert out["a/b"]["token"] == "value"


def test_error_json_shape():
    payload = json.loads(error_json("API Error", "boom"))
    assert payload == {"error": "API Error", "message": "boom"}


def test_confirmation_required_redacts_target():
    payload = json.loads(confirmation_required("POST /x", {"a": 1, "api_key": "provider-secret"}))
    assert payload["status"] == "confirmation_required"
    assert payload["action"] == "POST /x"
    assert payload["target"]["a"] == 1
    assert "provider-secret" not in json.dumps(payload)
