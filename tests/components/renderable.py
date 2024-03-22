from __future__ import annotations
from typing import *
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


# TODO Frame-by-frame interpolation instead of simple delays of animations
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

    # @property
    # def animation_map(self) -> AnimationMap:
    #     return self._animation_map

    # @animation_map.setter
    # def animation_map(self, value: AnimationMap) -> None:
    #     self._animation_map = value

    # @property
    # def animation(self) -> RenderIterable:
    #     return self._assets

    # @animation.setter
    # def animation(self, value: RenderIterable) -> None:
    #     self._assets = value

    def __post_init__(self) -> None:
        self.surface.fill(self.foreground)
        animations = load_image_directory(self.asset_path, self.alpha)

        self.animations = {}

        # for anim_key, mapping in animations.items():
        #     for frame_key, surface in mapping:
        #         self.animations[frame_key]

        # self.animations = {
        #     anim_key: RenderIterable(list(anim_dict.values()))
        #     for anim_key, anim_dict in animations.items()
        # }
        # debug(self.animations)

    def update(self) -> None:
        pass
        # self.surface.fill(self.foreground)

        # frame = next(self.animation)
        # frame = pyg.transform.scale(frame, (
        #     frame.get_width() * self.scale,
        #     frame.get_height() * self.scale,
        # ))

        # flags = pyg.BLEND_RGBA_MULT if self.alpha else 0
        # self.surface.blit(frame, (0, 0), special_flags=flags)
