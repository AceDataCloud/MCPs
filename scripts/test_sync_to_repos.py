"""Exercise source ownership and content reconciliation without network access."""

import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.sync_to_repos import load_mappings, mirror_contents


class SyncToReposTests(unittest.TestCase):
    def test_mapping_preserves_configured_workflow_ownership(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "first").mkdir()
            (root / "second").mkdir()
            (root / "sync.yaml").write_text(
                "mappings:\n  first:\n    repo: example/First\n    exclude: [.github]\n"
                "  second:\n    repo: example/Second\n    exclude: [.gitbooks]\n"
            )
            mappings = load_mappings(root)
            self.assertEqual(mappings["first"]["exclude"], [".github"])
            self.assertEqual(mappings["second"]["exclude"], [".gitbooks"])
            (root / "sync.yaml").write_text(
                "mappings:\n  ../escape:\n    repo: example/Bad\n"
            )
            with self.assertRaises(ValueError):
                load_mappings(root)

    @unittest.skipUnless(shutil.which("rsync"), "rsync is required by the sync runner")
    def test_content_changes_and_exclusions_are_honored(self):
        with tempfile.TemporaryDirectory() as temporary:
            source, target = (Path(temporary) / name for name in ("source", "target"))
            source.mkdir()
            target.mkdir()
            (source / "same-size").write_text("newer")
            (target / "same-size").write_text("older")
            # Equal mtimes and sizes must not cause a stale standalone copy.
            import os

            for path in (source / "same-size", target / "same-size"):
                os.utime(path, (1000000000, 1000000000))
            (target / "obsolete").write_text("delete")
            for name in (".git", ".github"):
                (target / name).mkdir()
                (target / name / "keep").write_text("standalone")
            mirror_contents(source, target, [".github"])
            self.assertEqual((target / "same-size").read_text(), "newer")
            self.assertFalse((target / "obsolete").exists())
            self.assertEqual((target / ".github/keep").read_text(), "standalone")
            self.assertEqual((target / ".git/keep").read_text(), "standalone")
            mirror_contents(source, target, [])
            self.assertFalse((target / ".github").exists())
