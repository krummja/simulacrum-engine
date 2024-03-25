from __future__ import annotations
from typing import *
from dataclasses import dataclass
from functools import cached_property
import pecs_framework as pecs

from pathlib import Path
import pygame as pyg

from simulacrum_engine.rendering.color import Color


@dataclass
class Renderable(pecs.Component):
    foreground: Color
    background: Color
    width: int = 12
    height: int = 18
    alpha: bool = True
    scale: float = 1.0

    @cached_property
    def surface(self) -> pyg.Surface:
        return pyg.Surface((self.width * self.scale, self.height * self.scale))

    def __post_init__(self) -> None:
        self.surface.fill(self.foreground)

    # def on_move_pressed(self, evt: pecs.EntityEvent) -> None:
    #     match evt.data.direction:
    #         case ["y", -1]:
    #             pass
    #         case ["y", 1]:
    #             pass
    #         case ["x", -1]:
    #             pass
    #         case ["x", 1]:
    #             pass

    # def on_move_released(self, evt: pecs.EntityEvent) -> None:
    #     match evt.data.direction:
    #         case ["y", -1]:
    #             pass
    #         case ["y", 1]:
    #             pass
    #         case ["x", -1]:
    #             pass
    #         case ["x", 1]:
    #             pass

    def update(self, frame: pyg.Surface) -> None:
        self.surface.fill(self.foreground)

        frame = pyg.transform.scale(frame, (
            frame.get_width() * self.scale,
            frame.get_height() * self.scale,
        ))

        flags = pyg.BLEND_RGBA_MULT if self.alpha else 0
        self.surface.blit(frame, (0, 0), special_flags=flags)
