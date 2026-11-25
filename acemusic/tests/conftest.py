"""Offline test environment."""

import os
import sys
from pathlib import Path

os.environ.setdefault("ACEDATACLOUD_API_TOKEN", "test-token")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
