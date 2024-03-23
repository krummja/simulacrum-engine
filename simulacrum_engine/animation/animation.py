from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from pathlib import Path
import pygame as pyg


class AnimationConfig(TypedDict):
    frame_delay: NotRequired[int]
    alpha: NotRequired[bool]


DEFAULT_ANIMATION_CONFIG = AnimationConfig({
    "frame_delay": 0,
    "alpha": True,
})


class Animation(Iterable):

    def __init__(
        self,
        values: list[pyg.Surface] | None = None,
        config: AnimationConfig = DEFAULT_ANIMATION_CONFIG,
    ) -> None:
        self._values = values if values else []
        self._config = config
        self._frame_count = config["frame_delay"]
        self._index = 0

    @property
    def config(self) -> AnimationConfig:
        return self._config

    def append(self, value: pyg.Surface) -> None:
        self._values.append(value)

    def __iter__(self) -> Iterator[pyg.Surface]:
        yield from self._values

    def __next__(self) -> pyg.Surface:
        self._frame_count -= 1

        if self._frame_count <= 1:
            self._index += 1
            self._frame_count = self._config["frame_delay"]

        if self._index >= len(self._values):
            self._index = 0

        return self._values[self._index]


class Animator:

    def __init__(self, animation: Animation, surface: pyg.Surface) -> None:
        self.animation = animation
        self.surface = surface
        self._is_playing = False

    def play(self) -> None:
        self._is_playing = True

    def stop(self) -> None:
        self._is_playing = False

    def update(self, scale: float = 1.0) -> None:
        if not self._is_playing:
            return

        frame = next(self.animation)
        frame = pyg.transform.scale(frame, (
            frame.get_width() * scale,
            frame.get_height() * scale,
        ))

        flags = pyg.BLEND_RGBA_MULT if self.animation.config["alpha"] else 0
        self.surface.blit(frame, (0, 0), special_flags=flags)
