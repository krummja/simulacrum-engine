from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from pathlib import Path
from enum import StrEnum


class AssetType(StrEnum):
    ANIMATION = "ANIMATION"
    AUDIO = "AUDIO"
    FONT = "FONT"
    PECS_PREFAB = "PECS_PREFAB"
    SCRIPT = "SCRIPT"
    SHADER = "SHADER"
    SPRITESHEET = "SPRITESHEET"
    TEXTURE = "TEXTURE"


class Asset:

    def __init__(self, path: Path, asset_type: AssetType) -> None:
        self.path = path
        self.asset_type = asset_type

    def load(self) -> None:
        pass
