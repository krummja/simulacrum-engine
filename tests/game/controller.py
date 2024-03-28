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
    state_name: str


class ControllerSystem(System):

    def initialize(self) -> None:
        self.input = self.engine[InputManager]
        self.query("controllables", all_of=[
            components.Controllable,
            components.Position,
            components.Velocity,
        ])

        self.input_vector = pyg.Vector2(0, 0)

    @cached_property
    def bindings(self) -> list[ControlBinding]:
        return [
            ControlBinding("W", ("y", -1), "move+up"),
            ControlBinding("A", ("x", -1), "move+left"),
            ControlBinding("S", ("y", 1), "move+down"),
            ControlBinding("D", ("x", 1), "move+right"),
        ]

    def update(self) -> None:
        controllables = self._queries["controllables"].result

        speed = 200
        dt = self.engine[WindowManager].delta

        for entity in controllables:
            position = entity[components.Position]
            velocity = entity[components.Velocity]

            for binding in self.bindings:
                if self.input.keyboard.pressed(binding.key):
                    entity.fire_event("request_state", data={
                        "state_name": binding.state_name,
                    })

                if self.input.keyboard.holding(binding.key):
                    input_value = binding.direction[1]
                    if binding.direction[0] == "x":
                        self.input_vector.x = input_value
                    if binding.direction[0] == "y":
                        self.input_vector.y = input_value

                if self.input.keyboard.released(binding.key):
                    if binding.direction[0] == "x":
                        self.input_vector.x = 0
                    if binding.direction[0] == "y":
                        self.input_vector.y = 0
                    if self.input_vector.x == 0 and self.input_vector.y == 0:
                        entity.fire_event("request_state", data={
                            "state_name": "idle",
                        })

            move_direction = self.input_vector
            if move_direction.magnitude() != 0:
                move_direction = move_direction.normalize()

            velocity.x = move_direction.x * speed
            velocity.y = move_direction.y * speed

            position.x += velocity.x * dt
            position.y += velocity.y * dt
