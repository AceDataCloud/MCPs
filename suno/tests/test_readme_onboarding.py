from __future__ import annotations

from pathlib import Path

README = (Path(__file__).resolve().parents[1] / "README.md").read_text()


def test_first_call_signup_is_attributed() -> None:
    url = (
        "https://platform.acedata.cloud/"
        "?utm_source=github&utm_medium=repo&utm_campaign=mcp-suno-first-call"
    )
    assert README.count(url) == 1


def test_first_call_uses_read_only_model_discovery() -> None:
    section = README.split("### 3. Verify the Connection", 1)[1].split("### 4. Or Run Locally", 1)[
        0
    ]
    assert "suno_list_models" in section
    assert "suno_list_custom_models" in section
    assert "limit=1" in section
    assert "even an empty list" in section
    assert "Both checks are free" in section
    assert "401 / 403" in section
    assert "trace_id" in section
    assert "suno_generate_music" not in section
