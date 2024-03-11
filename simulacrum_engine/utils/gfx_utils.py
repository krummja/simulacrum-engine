from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import pygame as pyg
from pygame import Surface
from pygame import Rect
# from pygame import Color

from simulacrum_engine.color import Color


def clip(surf: Surface, rect: Rect | tuple) -> Surface:
    if isinstance(rect, tuple):
        rect = Rect(*rect)
    surf.set_clip(rect)
    image = surf.subsurface(surf.get_clip()).copy()
    surf.set_clip(None)
    return image


def palette_swap(surf: Surface, colors: dict[Color, Color]) -> Surface:
    colorkey = surf.get_colorkey()
    surf = surf.copy()

    for from_color, to_color in colors.items():
        surf.set_colorkey(from_color)
        if len(to_color) <= 3:
            dest = Surface(surf.get_size())
        else:
            dest = Surface(surf.get_size(), pyg.SRCALPHA)

        dest.fill(to_color)
        dest.blit(surf, (0, 0))
        surf = dest

    surf.set_colorkey(colorkey)
    return surf
