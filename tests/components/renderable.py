from __future__ import annotations
from typing import *
from dataclasses import dataclass
from functools import cached_property
import pecs_framework as pecs

from pathlib import Path
import pygame as pyg

from simulacrum_engine.rendering.color import Color


class RenderIterable(Iterable):

    def __init__(
        self,
        initial_values: list[pyg.Surface],
        frame_delay: int = 0,
    ) -> None:
        self.values = initial_values
        self.frame_delay = frame_delay
        self.idx = 0
        self.frame_count = self.frame_delay

    def append(self, value: pyg.Surface) -> None:
        self.values.append(value)

    def __iter__(self) -> Iterator[pyg.Surface]:
        yield from self.values

    def __next__(self) -> pyg.Surface:
        self.frame_count -= 1

        if self.frame_count <= 1:
            self.idx += 1
            self.frame_count = self.frame_delay

        if self.idx >= len(self.values):
            self.idx = 0

        asset = self.values[self.idx]
        return asset


@dataclass
class Renderable(pecs.Component):
    asset_path: Path
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

    def on_move_pressed(self, evt: pecs.EntityEvent) -> None:
        match evt.data.direction:
            case ["y", -1]:
                pass
            case ["y", 1]:
                pass
            case ["x", -1]:
                pass
            case ["x", 1]:
                pass

    def on_move_released(self, evt: pecs.EntityEvent) -> None:
        match evt.data.direction:
            case ["y", -1]:
                pass
            case ["y", 1]:
                pass
            case ["x", -1]:
                pass
            case ["x", 1]:
                pass

    def update(self) -> None:
        self.surface.fill(self.foreground)

        # frame = next(self.animation)
        # frame = pyg.transform.scale(frame, (
        #     frame.get_width() * self.scale,
        #     frame.get_height() * self.scale,
        # ))

        # flags = pyg.BLEND_RGBA_MULT if self.alpha else 0
        # self.surface.blit(frame, (0, 0), special_flags=flags)
