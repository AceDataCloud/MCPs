"""Verify distribution without altering local OAuth variants."""

import tempfile
import unittest
from pathlib import Path

from scripts.sync_oauth import (
    DEPLOY_SERVERS,
    DEPLOY_SOURCE,
    HEADER,
    LOCAL_SERVERS,
    SHARED_SERVERS,
    SOURCE,
    STATE_HEADER,
    STATE_SERVERS,
    STATE_SOURCE,
    sync,
)


class SyncOAuthTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        source = self.root / SOURCE
        source.parent.mkdir()
        source.write_text('"""Shared provider."""\nVALUE = 1\n')
        (self.root / STATE_SOURCE).write_text('"""Shared store."""\nVALUE = 2\n')
        (self.root / DEPLOY_SOURCE).write_text("#!/bin/sh\necho shared\n")
        for server in set(SHARED_SERVERS) | LOCAL_SERVERS.keys():
            path = self.root / server / "core/oauth.py"
            path.parent.mkdir(parents=True)
            path.write_text(f"# Original {server}\n")

    def test_generation_is_idempotent_and_preserves_local_variants(self):
        local_before = {
            server: (self.root / server / "core/oauth.py").read_bytes()
            for server in LOCAL_SERVERS
        }
        self.assertEqual(
            len(sync(self.root)),
            len(SHARED_SERVERS) + len(STATE_SERVERS) + len(DEPLOY_SERVERS),
        )
        self.assertEqual(sync(self.root), [])
        expected = HEADER.encode() + (self.root / SOURCE).read_bytes()
        for server in SHARED_SERVERS:
            self.assertEqual(
                (self.root / server / "core/oauth.py").read_bytes(), expected
            )
        for server, content in local_before.items():
            self.assertEqual(
                (self.root / server / "core/oauth.py").read_bytes(), content
            )
        expected_state = STATE_HEADER.encode() + (self.root / STATE_SOURCE).read_bytes()
        for server in STATE_SERVERS:
            self.assertEqual(
                (self.root / server / "core/oauth_state.py").read_bytes(),
                expected_state,
            )
        for server in DEPLOY_SERVERS:
            self.assertEqual(
                (self.root / server / "deploy/oauth-state.sh").read_bytes(),
                (self.root / DEPLOY_SOURCE).read_bytes(),
            )

    def test_check_detects_manual_edits_without_writing(self):
        sync(self.root)
        relative = Path("suno/core/oauth.py")
        (self.root / relative).write_text("# manual change\n")
        self.assertEqual(sync(self.root, check=True), [relative])
        self.assertEqual((self.root / relative).read_text(), "# manual change\n")

    def test_shared_source_change_requires_all_consumers_to_update(self):
        sync(self.root)
        (self.root / SOURCE).write_text("VALUE = 2\n")
        self.assertEqual(len(sync(self.root, check=True)), len(SHARED_SERVERS))

    def test_shared_state_change_requires_all_consumers_to_update(self):
        sync(self.root)
        (self.root / STATE_SOURCE).write_text("VALUE = 3\n")
        self.assertEqual(len(sync(self.root, check=True)), len(STATE_SERVERS))

    def test_shared_deploy_change_requires_all_consumers_to_update(self):
        sync(self.root)
        (self.root / DEPLOY_SOURCE).write_text("#!/bin/sh\necho changed\n")
        self.assertEqual(len(sync(self.root, check=True)), len(DEPLOY_SERVERS))

    def test_unclassified_or_missing_server_fails_before_writing(self):
        original = (self.root / "suno/core/oauth.py").read_bytes()
        unexpected = self.root / "new-server/core/oauth.py"
        unexpected.parent.mkdir(parents=True)
        unexpected.write_text("# new provider\n")
        with self.assertRaisesRegex(ValueError, "Unclassified:.*new-server"):
            sync(self.root)
        self.assertEqual((self.root / "suno/core/oauth.py").read_bytes(), original)
        unexpected.unlink()
        (self.root / "happyhorse/core/oauth.py").unlink()
        with self.assertRaisesRegex(ValueError, "missing:.*happyhorse"):
            sync(self.root)
        self.assertEqual((self.root / "suno/core/oauth.py").read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
