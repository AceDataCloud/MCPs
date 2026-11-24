"""Publishing jobs must not call the retired Smithery API."""

import unittest
from pathlib import Path


class SmitheryReleaseTest(unittest.TestCase):
    def test_managed_smithery_publishing_is_retired(self):
        root = Path(__file__).resolve().parents[1]
        for workflow in root.glob("*/.github/workflows/*.y*ml"):
            with self.subTest(path=workflow.relative_to(root)):
                contents = workflow.read_text()
                self.assertNotIn("  publish-smithery:", contents)
                self.assertNotIn("@smithery/cli", contents)


if __name__ == "__main__":
    unittest.main()
