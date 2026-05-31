"""Pytest configuration and fixtures."""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load .env file BEFORE any other imports
from dotenv import load_dotenv  # noqa: E402

load_dotenv(dotenv_path=project_root / ".env")

# Set default log level for tests
os.environ.setdefault("LOG_LEVEL", "DEBUG")
