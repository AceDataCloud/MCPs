"""Type definitions for Face Transform MCP server."""

from typing import Literal

# Face analyze mode — 0 returns all faces, 1 returns the largest face only.
FaceAnalyzeMode = Literal[0, 1]

# Face model algorithm version (used by /face/analyze).
FaceModelVersion = Literal["1.0", "2.0", "3.0"]

# Optional rotate-detection toggle on /face/analyze.
FaceRotateDetection = Literal[0, 1]

# Default analyze mode (all faces detected).
DEFAULT_ANALYZE_MODE: FaceAnalyzeMode = 0

# Recommended face model algorithm version.
DEFAULT_MODEL_VERSION: FaceModelVersion = "3.0"
