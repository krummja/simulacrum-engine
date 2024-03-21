from __future__ import annotations
from typing import Iterable, Iterator
from dataclasses import dataclass, field
from functools import cached_property
from collections import OrderedDict
import pecs_framework as pecs

from pathlib import Path
import pygame as pyg

from simulacrum_engine.core.rendering.color import Color
from simulacrum_engine.core.assets.asset_utils import load_image
from simulacrum_engine.core.assets.asset_utils import load_image_directory

from devtools import debug


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
    alpha: bool = False
    scale: float = 1.0

    @cached_property
    def surface(self) -> pyg.Surface:
        return pyg.Surface((12 * self.scale, 18 * self.scale))

    @property
    def assets(self) -> RenderIterable:
        return self._assets

    @assets.setter
    def assets(self, value: RenderIterable) -> None:
        self._assets = value

    def __post_init__(self) -> None:
        self.assets = RenderIterable([], 30)

        for texture in load_image_directory(self.asset_path).values():
            self.assets.append(texture)

        self.surface.fill(self.foreground)

    def update(self) -> None:
        self.surface.fill(self.foreground)
        asset = next(self.assets)
        asset = pyg.transform.scale(asset, (
            asset.get_width() * self.scale,
            asset.get_height() * self.scale,
        ))

        flags = pyg.BLEND_RGBA_MULT if self.alpha else 0
        self.surface.blit(asset, (0, 0), special_flags=flags)
