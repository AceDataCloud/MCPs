"""Public ACE Music model contract."""

from typing import Literal

AceMusicModel = Literal["acemusic-v1.1", "acemusic-v1"]
DEFAULT_MODEL: AceMusicModel = "acemusic-v1.1"
