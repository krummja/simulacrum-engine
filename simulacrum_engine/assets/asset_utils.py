from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import os
import pygame as pyg
from pathlib import Path

from simulacrum_engine.rendering.color import Color
from devtools import debug


def load_image(path: Path, alpha: bool = False, colorkey=None) -> pyg.Surface:
    if alpha:
        image = pyg.image.load(path).convert_alpha()
    else:
        image = pyg.image.load(path).convert()
    if colorkey:
        image.set_colorkey(colorkey)
    return image


def load_sound(path: Path):
    pass


def load_animation(path: Path):
    pass
