from __future__ import annotations
from typing import *

from pathlib import Path
import pygame as pyg

from simulacrum_engine.rendering.color import Color
from simulacrum_engine.rendering import gfx_tools
from simulacrum_engine.assets import asset_utils


class Spritesheet:

    def __init__(self) -> None:
        self.tiles: dict[tuple[int, int], pyg.Surface] = {}

    def parse(self, surface: pyg.Surface, split_color: Color) -> Self:
        location = [0, 0]
        row_start = None

        for y in range(surface.get_height() - 1):

            sample1 = surface.get_at((1, y))
            sample2 = surface.get_at((1, y + 1))
            sample3 = surface.get_at((0, y + 1))

            if sample1 == sample3 == split_color != sample2:
                row_start = y

            if sample1 != split_color == sample2 == sample3 and row_start is not None:
                row_bounds_y = (row_start, y)
                col_start = None

                for x in range(surface.get_width() - 1):
                    sample4 = surface.get_at((x, row_bounds_y[0] + 1))
                    sample5 = surface.get_at((x + 1, row_bounds_y[0] + 1))

                    if sample4 == split_color != sample5:
                        col_start = x

                    if sample4 != split_color == sample5 and col_start is not None:
                        col_bounds_x = (col_start, x)

                        if col_start == 0:
                            tile_bounds_y = row_bounds_y

                        else:
                            y2 = row_start
                            while True:
                                sample6 = surface.get_at((col_start + 1, y2))
                                sample7 = surface.get_at((col_start + 1, y2 + 1))

                                if sample6 != split_color == sample7:
                                    break
                                y2 += 1

                            tile_bounds_y = (row_start, y2)

                        rect = pyg.Rect(
                            col_bounds_x[0] + 1,
                            tile_bounds_y[0] + 1,
                            col_bounds_x[1] - col_bounds_x[0],
                            tile_bounds_y[1] - tile_bounds_y[0],
                        )

                        addr = (location[0], location[1])
                        self.tiles[addr] = gfx_tools.clip(surface, rect)
                        location[0] += 1
                        col_start = None

                location[1] += 1
                location[0] = 0
                row_start = None

        return self
