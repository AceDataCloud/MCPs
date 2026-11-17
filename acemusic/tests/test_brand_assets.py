"""Pinned official build assets, independent of network availability."""

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "fetch_brand_assets", ROOT / "scripts/fetch_brand_assets.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_digest_rejects_non_png_and_changed_bytes():
    data = MODULE.PNG_SIGNATURE + b"fixture"
    digest = hashlib.sha256(data).hexdigest()
    assert MODULE.verified_icon(data, digest) == data
    with pytest.raises(ValueError, match="SHA256"):
        MODULE.verified_icon(data, "0" * 64)
    with pytest.raises(ValueError, match="PNG"):
        MODULE.verified_icon(b"html", digest)


def test_verified_cached_icon_materializes_both_packagers(tmp_path):
    data = MODULE.PNG_SIGNATURE + b"fixture"
    (tmp_path / "brand-assets.json").write_text(
        json.dumps(
            {
                "icon": {
                    "url": "https://cdn.acedata.cloud/immutable.png",
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            }
        )
    )
    (tmp_path / "vscode").mkdir()
    (tmp_path / "vscode/icon.png").write_bytes(data)
    MODULE.prepare_assets("all", tmp_path)
    destination = tmp_path / "jetbrains/src/main/resources/META-INF"
    assert (destination / "pluginIcon.png").read_bytes() == data
    assert "data:image/png;base64," in (destination / "pluginIcon.svg").read_text()


def test_manifest_pins_official_cdn_and_download_build_hooks():
    icon = json.loads((ROOT / "brand-assets.json").read_text())["icon"]
    assert icon["source_url"] == "https://acemusic.ai/public/assets/favicon-192.png"
    assert icon["url"] == "https://cdn.acedata.cloud/acemusic-icon-52deddfc87b9.png"
    package = json.loads((ROOT / "vscode/package.json").read_text())
    assert "fetch_brand_assets.py" in package["scripts"]["vscode:prepublish"]
    assert (
        "dependsOn(prepareOfficialBrandIcon)" in (ROOT / "jetbrains/build.gradle.kts").read_text()
    )
