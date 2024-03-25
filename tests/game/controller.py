from __future__ import annotations
from typing import *

from functools import cached_property

import pygame as pyg
from simulacrum_engine import *
from simulacrum_engine.ecs.system import System

from tests import components


class ControlBinding(NamedTuple):
    key: str
    direction: tuple[Literal["x"] | Literal["y"], int]


class ControllerSystem(System):

    def initialize(self) -> None:
        self.input = self.engine[InputManager]
        self.query("controllables", all_of=[
            components.Controllable,
            components.Position,
        ])

    @cached_property
    def bindings(self) -> list[ControlBinding]:
        return [
            ControlBinding("W", ("y", -1)),
            ControlBinding("A", ("x", -1)),
            ControlBinding("S", ("y", 1)),
            ControlBinding("D", ("x", 1)),
        ]

    def update(self) -> None:
        controllables = self._queries["controllables"].result

        speed = 200
        dt = self.engine[WindowManager].delta

        for entity in controllables:
            position = entity[components.Position]
            input_vector = pyg.Vector2(0, 0)

            for binding in self.bindings:
                if self.input.keyboard.pressed(binding.key):
                    entity.fire_event("move_pressed", data={
                        "direction": binding.direction,
                    })

                if self.input.keyboard.holding(binding.key):
                    setattr(input_vector, *binding.direction)

                if self.input.keyboard.released(binding.key):
                    entity.fire_event("move_released", data={
                        "direction": binding.direction,
                    })

            move_direction = pyg.Vector2(input_vector.x, input_vector.y)
            magnitude = move_direction.magnitude()

            if magnitude != 0:
                move_direction = move_direction.normalize()

            position.x += move_direction.x * speed * dt
            position.y += move_direction.y * speed * dt
