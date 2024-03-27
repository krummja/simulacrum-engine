from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import pygame as pyg


class AnimationConfig(TypedDict):
    frame_delay: NotRequired[int]
    alpha: NotRequired[bool]
    can_mirror: NotRequired[bool]


DEFAULT_ANIMATION_CONFIG = AnimationConfig({
    "frame_delay": 0,
    "alpha": True,
    "can_mirror": False,
})


class InvalidPathException(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class Animation(Iterable):
    """
    A simple iterable of frames with some optional config.

    Points to a filesystem path to load frames from and optionally takes in an
    `AnimationConfig` object. If no config is passed, defaults will be used.
    """

    def __init__(
        self,
        name: str,
        frames: list[pyg.Surface],
        config: AnimationConfig | None = None,
    ) -> None:
        self.name = name
        self._frames = frames

        if config is None:
            config = DEFAULT_ANIMATION_CONFIG
        else:
            config = DEFAULT_ANIMATION_CONFIG | config

        self._config = config
        self._frame_count = config["frame_delay"]
        self._index = 0

    @property
    def config(self) -> AnimationConfig:
        return self._config

    def reset(self) -> None:
        self._index = 0

    def __iter__(self) -> Iterator[pyg.Surface]:
        yield from self._frames

    def __next__(self) -> pyg.Surface:
        self._frame_count -= 1

        if self._frame_count <= 1:
            self._index += 1
            self._frame_count = self._config["frame_delay"]

        if self._index >= len(self._frames):
            self._index = 0

        return self._frames[self._index]


class Animator:
    """
    An `Animator` wraps a single animation and exposes a control surface for
    manipulating the animation's state. An `Animation` instance, which holds
    reference to a sequence of images making up the animation frames, is used to
    iteratively blit to the bound PyGame `Surface` object.
    """

    def __init__(self, animation: Animation, surface: pyg.Surface) -> None:
        self.animation = animation
        self.surface = surface
        self._is_playing = False

    def play(self, flipped_h: bool = False, flipped_v: bool = False) -> None:
        pyg.transform.flip(self.surface, flipped_h, flipped_v)
        self._is_playing = True

    def pause(self) -> None:
        self._is_playing = False

    def stop(self) -> None:
        self._is_playing = False
        self.animation.reset()
