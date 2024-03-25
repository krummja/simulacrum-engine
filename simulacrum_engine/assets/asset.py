from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from simulacrum_engine.animation import Animation
import pygame as pyg

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


_AssetType = Animation | pyg.Surface | list[Animation] | list[pyg.Surface]
AT = TypeVar("AT", bound=_AssetType)


class Asset(Generic[AT]):

    def __init__(
        self,
        name: str,
        path: Path,
        asset_type: AssetType,
        contents: AT,
    ) -> None:
        self.name = name
        self.path = path
        self.asset_type = asset_type
        self._contents = contents

    def unwrap(self) -> AT:
        return self._contents
