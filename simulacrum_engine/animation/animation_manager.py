from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from collections import deque
import pygame as pyg

from simulacrum_engine.component import EngineComponent
from simulacrum_engine.events import Events

from simulacrum_engine.animation import Animator


class AnimationJob(NamedTuple):
    entity: str
    animation: str


class AnimatorRegistry:

    def __init__(self) -> None:
        self._mapping = {}

    def __getitem__(self, entity: str) -> dict[str, Animator]:
        return self._mapping.get(entity, None)

    @property
    def mapping(self) -> dict[str, dict[str, Animator]]:
        return self._mapping

    def get_animators_for(self, entity: str) -> dict[str, Animator]:
        return self._mapping.get(entity, {})

    def add(self, entity: str, animation: str, animator: Animator) -> None:
        if entity not in self._mapping:
            self._mapping[entity] = {}
        self._mapping[entity][animation] = animator

    def remove(self, entity: str, animation: str | None = None) -> None:
        if animation is None:
            del self._mapping[entity]
        else:
            del self._mapping[entity][animation]


class AnimationManager(EngineComponent):

    def boot(self) -> bool:
        self._registry = AnimatorRegistry()
        return True

    def ready(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def play(self, entity: str, animation: str) -> None:
        animator = self._registry.mapping[entity][animation]
        animator.play()

    def pause(self, entity: str, animation: str) -> None:
        animator = self._registry.mapping[entity][animation]
        animator.pause()

    def stop(self, entity: str, animation: str) -> None:
        animator = self._registry.mapping[entity][animation]
        animator.stop()

    def play_all(self) -> None:
        for animators in self._registry.mapping.values():
            for animator in animators.values():
                animator.play()

    def stop_all(self) -> None:
        for animators in self._registry.mapping.values():
            for animator in animators.values():
                animator.stop()

    def add(self, entity: str, animation: str, animator: Animator) -> None:
        self._registry.add(entity, animation, animator)

    def remove(self, entity: str, animation: str | None = None) -> None:
        self._registry.remove(entity, animation)
