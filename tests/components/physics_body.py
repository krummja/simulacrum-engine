from __future__ import annotations

from dataclasses import dataclass
import pecs_framework as pecs
import pygame as pyg
import pymunk as pym


@dataclass
class PhysicsBody(pecs.Component):
    mass: float

    def __post_init__(self) -> None:
        self._body = pym.Body(mass=self.mass)
        self._added = False

    @property
    def body(self) -> pym.Body:
        return self._body

    @property
    def is_added(self) -> bool:
        return self._added

    def add(self) -> pym.Body:
        self._added = True
        return self._body
