import json
import unittest
from unittest.mock import patch

from scripts.retire_registry_sora import (
    OFFICIAL,
    SERVER,
    assert_frozen,
    oidc_registry_token,
    retire,
    versions,
)


def row(version, status, name=SERVER):
    return {
        "server": {"name": name, "version": version},
        "_meta": {OFFICIAL: {"status": status}},
    }


class RetirementTest(unittest.TestCase):
    def test_freeze_required(self):
        assert_frozen("jobs:\n  build:\n    # retired\n    if: ${{ false }}\n", "build")
        with self.assertRaises(RuntimeError):
            assert_frozen("jobs:\n  build:\n    if: true\n", "build")

    @patch(
        "scripts.retire_registry_sora.request_json",
        return_value={"servers": [row("1", "active", "io.github.other/server")]},
    )
    def test_rejects_other_server(self, request):
        with self.assertRaises(RuntimeError):
            versions()

    @patch("scripts.retire_registry_sora.request_json")
    def test_inventory_pagination_and_repeat_guard(self, request):
        request.side_effect = [
            {"servers": [row("1", "active")], "metadata": {"nextCursor": "a+b"}},
            {"servers": [row("2", "deleted")]},
        ]
        self.assertEqual(versions(), {"1": "active", "2": "deleted"})
        self.assertIn("cursor=a%2Bb", request.call_args.args[0])
        request.side_effect = None
        request.return_value = {"metadata": {"nextCursor": "same"}}
        with self.assertRaises(RuntimeError):
            versions()

    @patch(
        "scripts.retire_registry_sora.verify_freeze",
        return_value={"mirror_frozen": True},
    )
    @patch("scripts.retire_registry_sora.versions", return_value={"1": "active"})
    @patch("scripts.retire_registry_sora.oidc_registry_token")
    @patch("scripts.retire_registry_sora.request_json")
    def test_dry_run_does_not_authenticate_or_write(
        self, request, token, inventory, freeze
    ):
        report = {}
        retire(report, False)
        self.assertEqual(report["status"], "dry-run")
        token.assert_not_called()
        request.assert_not_called()

    @patch(
        "scripts.retire_registry_sora.verify_freeze",
        side_effect=RuntimeError("not frozen"),
    )
    @patch("scripts.retire_registry_sora.oidc_registry_token")
    def test_freeze_failure_blocks_before_identity(self, token, freeze):
        with self.assertRaises(RuntimeError):
            retire({}, True)
        token.assert_not_called()

    @patch("scripts.retire_registry_sora.verify_freeze", return_value={})
    @patch(
        "scripts.retire_registry_sora.versions",
        side_effect=[
            {"a": "active", "d": "deleted", "old": "deprecated"},
            {"a": "deprecated", "d": "deleted", "old": "deprecated"},
        ],
    )
    @patch(
        "scripts.retire_registry_sora.oidc_registry_token", return_value="fixture-token"
    )
    @patch("scripts.retire_registry_sora.request_json")
    def test_only_active_existing_version_is_deprecated(
        self, request, token, inventory, freeze
    ):
        request.side_effect = [row("a", "active"), {}]
        report = {}
        retire(report, True)
        self.assertEqual(report["changed_versions"], ["a"])
        patches = [
            c for c in request.call_args_list if c.kwargs.get("method") == "PATCH"
        ]
        self.assertEqual(len(patches), 1)
        self.assertTrue(patches[0].args[0].endswith("/versions/a/status"))
        self.assertEqual(patches[0].kwargs["body"]["status"], "deprecated")
        self.assertNotIn("fixture-token", json.dumps(report))

    @patch.dict(
        "os.environ",
        {
            "GITHUB_REPOSITORY": "other/repo",
            "GITHUB_REF": "refs/heads/main",
            "GITHUB_EVENT_NAME": "workflow_dispatch",
        },
        clear=True,
    )
    @patch("scripts.retire_registry_sora.request_json")
    def test_apply_identity_cannot_run_from_other_repository(self, request):
        with self.assertRaises(RuntimeError):
            oidc_registry_token()
        request.assert_not_called()
