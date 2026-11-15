import unittest
from pathlib import Path

import yaml


class QwenOAuthClientTests(unittest.TestCase):
    def test_qwen_callback_uses_its_own_client(self):
        root = Path(__file__).resolve().parents[1]
        def env(server):
            manifest = yaml.safe_load((root / server / "deploy/production/deployment.yaml").read_text())
            return {entry["name"]: entry.get("value") for entry in manifest["spec"]["template"]["spec"]["containers"][0]["env"]}
        qwen = env("qwen-image")
        seedream = env("seedream")
        self.assertNotEqual(qwen["ACEDATACLOUD_OAUTH_CLIENT_ID"], seedream["ACEDATACLOUD_OAUTH_CLIENT_ID"])
        self.assertEqual(qwen["MCP_SERVER_URL"], "https://qwen-image.mcp.acedata.cloud")


if __name__ == "__main__":
    unittest.main()
