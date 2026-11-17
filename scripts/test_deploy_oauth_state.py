"""Explicit bootstrap preserves established key material without running deploys."""

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.bootstrap_oauth_state import bootstrap


class DeployOAuthStateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "scripts").mkdir()
        (self.root / "scripts/mcp_catalog.json").write_text(
            '{"services": {"test": {"status": "active"}}}\n'
        )
        self.package = self.root / "test/deploy/production"
        self.package.mkdir(parents=True)
        (self.package / "deployment.yaml").write_text(
            "metadata:\n  name: mcp-test\n  namespace: acedatacloud\n"
        )
        self.secret = {}
        self.deployment = {}
        self.pvc = {}
        self.created = []
        self.unreachable = False
        self.mock = patch(
            "scripts.bootstrap_oauth_state.subprocess.run", side_effect=self.kubectl
        )
        self.mock.start()
        self.addCleanup(self.mock.stop)

    def kubectl(self, args, **kwargs):
        self.assertEqual(
            args[:5], ["kubectl", "--context", "reviewed", "-n", "acedatacloud"]
        )
        operation = args[5:]
        if self.unreachable:
            return subprocess.CompletedProcess(args, 1, "", "unavailable")
        if operation[0] == "get":
            import json

            state = {
                "secret": self.secret,
                "deployment": self.deployment,
                "pvc": self.pvc,
            }[operation[1]]
            return subprocess.CompletedProcess(
                args, 0, json.dumps(state) if state else "", ""
            )
        self.assertEqual(operation[:3], ["create", "secret", "generic"])
        self.created.append(operation[3])
        self.secret = {"data": {"state_key": "unchanged", "password": "unchanged"}}
        return subprocess.CompletedProcess(args, 0, "created", "")

    def test_creates_once_then_preserves_existing_key(self):
        bootstrap("test", "reviewed", self.root)
        bootstrap("test", "reviewed", self.root)
        self.assertEqual(self.created, ["mcp-test-oauth-state"])
        self.assertEqual(self.secret["data"]["state_key"], "unchanged")

    def test_missing_key_with_existing_deployment_requires_restore(self):
        self.deployment = {"metadata": {"name": "mcp-test"}}
        with self.assertRaisesRegex(RuntimeError, "restore mcp-test-oauth-state"):
            bootstrap("test", "reviewed", self.root)
        self.assertEqual(self.created, [])

    def test_shared_redis_pvc_refuses_silent_key_rotation(self):
        (self.package / "oauth-redis.yaml").write_text("kind: StatefulSet\n")
        self.pvc = {"metadata": {"name": "data-mcp-acedatacloud-oauth-redis-0"}}
        with self.assertRaisesRegex(
            RuntimeError, "restore mcp-acedatacloud-oauth-redis"
        ):
            bootstrap("test", "reviewed", self.root)
        self.assertEqual(self.created, [])

    def test_incomplete_or_unreadable_secret_does_not_generate_key(self):
        self.secret = {"data": {}}
        with self.assertRaisesRegex(RuntimeError, "required key data is missing"):
            bootstrap("test", "reviewed", self.root)
        self.secret = {}
        self.unreachable = True
        with self.assertRaisesRegex(RuntimeError, "no key was generated"):
            bootstrap("test", "reviewed", self.root)
        self.assertEqual(self.created, [])
