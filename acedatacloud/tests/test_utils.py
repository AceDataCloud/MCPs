"""Unit tests for the utility helpers."""

import json

from core.utils import confirmation_required, dumps, error_json, mask_secrets


def test_mask_secrets_masks_token():
    data = {"token": "abcdef0123456789", "name": "ci"}
    masked = mask_secrets(data)
    assert masked["token"].endswith("chars)")
    assert "abcdef0123456789" not in masked["token"]
    assert masked["name"] == "ci"


def test_mask_secrets_short_value():
    assert mask_secrets({"password": "abc"})["password"] == "***"


def test_mask_secrets_reveal_passthrough():
    data = {"token": "abcdef0123456789"}
    assert mask_secrets(data, reveal=True) == data


def test_mask_secrets_nested_and_lists():
    data = {"items": [{"token": "x" * 20, "ok": 1}]}
    masked = mask_secrets(data)
    assert "x" * 20 not in json.dumps(masked)
    assert masked["items"][0]["ok"] == 1


def test_dumps_masks_by_default():
    out = dumps({"token": "abcdef0123456789"})
    assert "abcdef0123456789" not in out
    out_reveal = dumps({"token": "abcdef0123456789"}, reveal=True)
    assert "abcdef0123456789" in out_reveal


def test_error_json_shape():
    payload = json.loads(error_json("API Error", "boom"))
    assert payload == {"error": "API Error", "message": "boom"}


def test_confirmation_required_shape():
    payload = json.loads(confirmation_required("POST /x", {"a": 1}))
    assert payload["status"] == "confirmation_required"
    assert payload["action"] == "POST /x"
    assert payload["target"] == {"a": 1}
