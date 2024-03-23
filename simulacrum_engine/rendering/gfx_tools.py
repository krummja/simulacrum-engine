from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import pygame as pyg
from simulacrum_engine.rendering.color import Color


def clip(surf: pyg.Surface, rect: pyg.Rect | tuple) -> pyg.Surface:
    if isinstance(rect, tuple):
        rect = pyg.Rect(*rect)
    surf.set_clip(rect)
    image = surf.subsurface(surf.get_clip()).copy()
    surf.set_clip(None)
    return image


def palette_swap(surf: pyg.Surface, colors: dict[Color, Color]) -> pyg.Surface:
    colorkey = surf.get_colorkey()
    surf = surf.copy()

    for from_color, to_color in colors.items():
        surf.set_colorkey(from_color)
        if len(to_color) <= 3:
            dest = pyg.Surface(surf.get_size())
        else:
            dest = pyg.Surface(surf.get_size(), pyg.SRCALPHA)

        dest.fill(to_color)
        dest.blit(surf, (0, 0))
        surf = dest

    surf.set_colorkey(colorkey)
    return surf


def ease_approach(dt: float, val: float, target: float, drag: float = 1) -> float:
    val += (target - val) / drag * min(dt, drag)
    return val
