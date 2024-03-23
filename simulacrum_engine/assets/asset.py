from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import os
from pathlib import Path
from enum import StrEnum

from .asset_utils import load_image


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

    def __init__(self, asset_type: AssetType, path: Path | None = None) -> None:
        self.asset_type = asset_type

        if (ASSET_PATH := os.environ.get("ASSET_PATH")) and path is not None:
            self.path = Path(ASSET_PATH, path)
        else:
            self.path = path

    def load(self) -> None:
        raise NotImplementedError("This method has no implementation.")
