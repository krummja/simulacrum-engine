from __future__ import annotations
from typing import *
from dataclasses import dataclass
import pecs_framework as pecs

import pygame as pyg
from simulacrum_engine.assets import Asset
from simulacrum_engine.animation import Animation


@dataclass
class Animatable(pecs.Component):
    animations: dict[str, Asset[Animation]]
    start_animation: str

    def __post_init__(self) -> None:
        self._current_animation: str = self.start_animation
        self._current_frame: pyg.Surface | None = None

    @property
    def current_animation(self) -> Animation:
        return self.animations[self._current_animation].unwrap()

    @property
    def next_frame(self) -> pyg.Surface:
        return next(self.current_animation)

    def set_animation(self, animation: str) -> None:
        self._current_animation = animation
