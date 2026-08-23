import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.setdefault("LOG_LEVEL", "DEBUG")


@pytest.fixture
def api_token() -> str:
    return "test-token"
