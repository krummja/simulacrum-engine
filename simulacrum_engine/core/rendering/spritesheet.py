from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from pathlib import Path
import pygame as pyg

from simulacrum_engine.core.rendering.color import Color


class Spritesheet:

    def __init__(self, path: Path) -> None:
        self.path = path
        self.tiles: dict[str, pyg.Surface] = {}

    def parse(self, surface: pyg.Surface, split_color: Color) -> None:
        location = [0, 0]
        row_start = 0

        for y in range(surface.get_height() - 1):

            sample1 = surface.get_at((1, y))
            sample2 = surface.get_at((1, y + 1))
            sample3 = surface.get_at((0, y + 1))

            row_start = self.is_split(
                Color.from_pyg(sample1),
                Color.from_pyg(sample2),
                Color.from_pyg(sample3),
            )

            for x in range(surface.get_width() - 1):
                pass

    def is_split(self, left: Color, at: Color, right: Color) -> bool:
        return False
