"""Unit tests for pure helpers (no network)."""

from core.client import _unwrap
from tools.doc_tools import _doc_ref
from tools.example_tools import _example_body, _snippets


def test_unwrap_paginated_and_plain():
    assert _unwrap({"results": [1, 2], "count": 2}) == [1, 2]
    assert _unwrap([1, 2, 3]) == [1, 2, 3]
    assert _unwrap({"x": 1}) == {"x": 1}


def test_doc_ref_strips_url_to_alias():
    assert _doc_ref("https://platform.acedata.cloud/documents/suno-api") == "suno-api"
    assert _doc_ref("https://platform.acedata.cloud/documents/suno-api?x=1") == "suno-api"
    assert _doc_ref("  suno-api  ") == "suno-api"
    assert (
        _doc_ref("6f4872e5-d43a-4f3b-b645-86456830de49") == "6f4872e5-d43a-4f3b-b645-86456830de49"
    )


def test_doc_ref_rejects_traversal_and_query():
    # Path traversal / endpoint escape / query injection must all be rejected.
    assert _doc_ref("../apis/?private=true") == ""
    assert _doc_ref("..") == ""
    assert _doc_ref("a/b") == ""
    assert _doc_ref("foo?x=1") == ""
    assert _doc_ref("") == ""


def test_example_body_from_schema():
    definition = {
        "paths": {
            "/suno/audios": {
                "post": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "required": ["prompt"],
                                    "properties": {
                                        "prompt": {"type": "string", "example": "a pop song"},
                                        "model": {"type": "string", "enum": ["chirp-v4"]},
                                    },
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    body = _example_body(definition, "/suno/audios", "POST")
    assert body["prompt"] == "a pop song"
    assert body["model"] == "chirp-v4"


def test_snippets_have_all_three_languages():
    snips = _snippets("POST", "https://api.acedata.cloud/suno/audios", {"prompt": "x"})
    assert set(snips) == {"curl", "python", "javascript"}
    assert "Bearer YOUR_API_TOKEN" in snips["curl"]
    assert "api.acedata.cloud/suno/audios" in snips["python"]
