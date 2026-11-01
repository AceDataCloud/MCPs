"""Keep active deployment commands compatible with current hosted runners."""

import json
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class DeployWorkflowTests(unittest.TestCase):
    def test_active_deployments_do_not_require_legacy_compose_binary(self):
        catalog = json.loads((ROOT / "scripts/mcp_catalog.json").read_text())[
            "services"
        ]
        for alias, entry in catalog.items():
            if entry["status"] != "active":
                continue
            for path in (ROOT / alias / ".github/workflows").glob("deploy.y*"):
                workflow = yaml.safe_load(path.read_text())
                for job in workflow["jobs"].values():
                    for step in job.get("steps", []):
                        with self.subTest(alias=alias, step=step.get("name")):
                            self.assertNotRegex(
                                step.get("run", ""),
                                r"(?<![\w./-])docker-compose(?=\s|$)",
                                "Use the runner's Docker Compose v2 plugin.",
                            )


if __name__ == "__main__":
    unittest.main()
