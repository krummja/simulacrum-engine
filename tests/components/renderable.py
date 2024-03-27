from __future__ import annotations
from typing import *
from dataclasses import dataclass
from functools import cached_property
import pecs_framework as pecs

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
    flipped_h: bool = False
    flipped_v: bool = False

    @cached_property
    def surface(self) -> pyg.Surface:
        return pyg.Surface((self.width * self.scale, self.height * self.scale))

    def __post_init__(self) -> None:
        self.surface.fill(self.foreground)

    def update(self, frame: pyg.Surface) -> None:
        self.surface.fill(self.foreground)

        frame = pyg.transform.scale(frame, (
            frame.get_width() * self.scale,
            frame.get_height() * self.scale,
        ))

        frame = pyg.transform.flip(frame, self.flipped_h, self.flipped_v)

        flags = pyg.BLEND_RGBA_MULT if self.alpha else 0
        self.surface.blit(frame, (0, 0), special_flags=flags)

    def on_set_flipped(self, evt: pecs.EntityEvent) -> pecs.EntityEvent:
        if hasattr(evt.data, "flipped_h"):
            self.flipped_h = evt.data.flipped_h
        if hasattr(evt.data, "flipped_v"):
            self.flipped_v = evt.data.flipped_v
        return evt
