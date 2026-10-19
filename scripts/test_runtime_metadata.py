"""Prevent invalid icons, accidental identity changes, and projection drift."""

import ast
import copy
import tempfile
import unittest
from pathlib import Path

from scripts.mcp_catalog import load_catalog
from scripts.runtime_metadata import ROOT, render_server, runtime_icons, sync

ICON = {"src": "https://cdn.acedata.cloud/9q90dl.png", "mimeType": "image/png"}
SOURCE = b"""from mcp.server.fastmcp import FastMCP

kwargs = {"host": "0.0.0.0"}
mcp = FastMCP("same-name", **kwargs)
"""


def without_icons(source):
    tree = ast.parse(source)
    tree.body = [
        node
        for node in tree.body
        if not (isinstance(node, ast.ImportFrom) and node.module == "mcp.types")
    ]
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "FastMCP"
        ):
            node.keywords = [item for item in node.keywords if item.arg != "icons"]
    return ast.dump(tree)


class RuntimeMetadataTest(unittest.TestCase):
    def test_only_four_explicit_services_are_projected_and_copies_are_current(self):
        self.assertEqual(
            set(runtime_icons(load_catalog())),
            {"seedance", "nanobanana", "happyhorse", "openai"},
        )
        self.assertEqual(sync(check=True), [])
        for alias, icon in runtime_icons(load_catalog()).items():
            source = (ROOT / alias / "core/server.py").read_bytes()
            self.assertEqual(render_server(source, icon), source)

    def test_registry_profiles_do_not_supply_generic_runtime_identity(self):
        catalog = {"openai": {"status": "active", "registry_profiles": [{"icon": ICON}]}}
        self.assertEqual(runtime_icons(catalog), {})
        catalog["openai"]["runtime_icon"] = ICON
        self.assertEqual(runtime_icons(catalog), {"openai": ICON})

    def test_empty_control_whitespace_and_non_https_icons_fail_before_write(self):
        for src in [
            "",
            "\x01",
            "https://cdn.acedata.cloud/\x01.png",
            "https://cdn.acedata.cloud/a b.png",
            "http://example.com/a.png",
            "data:image/png,abc",
            "https:///a.png",
            "https://user:password@example.com/a.png",
        ]:
            with self.subTest(src=src), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for alias in ["seedance", "openai"]:
                    path = root / alias / "core/server.py"
                    path.parent.mkdir(parents=True)
                    path.write_bytes(SOURCE)
                catalog = {
                    "seedance": {"status": "active", "runtime_icon": ICON},
                    "openai": {
                        "status": "active",
                        "runtime_icon": {"src": src, "mimeType": "image/png"},
                    },
                }
                with self.assertRaises(ValueError):
                    sync(root, catalog=catalog)
                self.assertEqual((root / "seedance/core/server.py").read_bytes(), SOURCE)

    def test_explicit_registry_reference_requires_an_icon_and_valid_mime(self):
        for icon in [None, "profile", {"src": ICON["src"], "mimeType": "text/html"}]:
            entry = {
                "status": "active",
                "runtime_icon": "registry",
                "registry": {"icon": icon},
            }
            with self.subTest(icon=icon), self.assertRaises(ValueError):
                runtime_icons({"seedance": entry})

    def test_ast_projection_repairs_control_byte_without_touching_identity_or_auth(
        self,
    ):
        original = (b"from mcp.types import Icon\n" + SOURCE).replace(
            b"**kwargs", b'icons=[Icon(src="\x01", mimeType="image/png")], **kwargs'
        )
        fixed = render_server(original, ICON)
        self.assertIn(ICON["src"].encode(), fixed)
        self.assertNotIn(b"\x01", fixed)
        self.assertEqual(without_icons(original), without_icons(fixed))
        self.assertEqual(render_server(fixed, ICON), fixed)

    def test_insertion_unicode_and_missing_initialization_fail_closed(self):
        original = SOURCE.replace(b"same-name", "相同名称".encode())
        fixed = render_server(original, ICON)
        self.assertEqual(without_icons(original), without_icons(fixed))
        self.assertEqual(render_server(fixed, ICON), fixed)
        for source in [b"x = 1", SOURCE.replace(b"**kwargs", b"host='same'")]:
            with self.assertRaises(ValueError):
                render_server(source, ICON)

    def test_check_mode_does_not_write_and_retired_service_stays_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "seedance/core/server.py"
            path.parent.mkdir(parents=True)
            path.write_bytes(SOURCE)
            catalog = {"seedance": {"status": "active", "runtime_icon": ICON}}
            self.assertEqual(
                sync(root, check=True, catalog=catalog),
                [Path("seedance/core/server.py")],
            )
            self.assertEqual(path.read_bytes(), SOURCE)
            self.assertEqual(sync(root, catalog=catalog), [Path("seedance/core/server.py")])
            self.assertEqual(sync(root, catalog=catalog), [])
            retired = copy.deepcopy(catalog)
            retired["seedance"]["status"] = "retired"
            self.assertEqual(runtime_icons(retired), {})
