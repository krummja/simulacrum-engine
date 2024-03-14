from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from pathlib import Path
from simulacrum_engine.color import Color


class Asset:

    def __init__(self, path: Path) -> None:
        self.path = path
