from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from pecs_framework import Loader, BaseSystem
import pecs_framework as pecs

from functools import cached_property

import time
from pathlib import Path
from rich import inspect
from enum import StrEnum

import pygame as pyg
from simulacrum_engine import *
from simulacrum_engine.assets import Spritesheet
from simulacrum_engine.assets import asset_utils
from simulacrum_engine.ecs.loop import Loop
from simulacrum_engine.ecs.system import System

from tests import components
from tests import ui


class ControlBinding(NamedTuple):
    key: str
    direction: tuple[Literal["x"] | Literal["y"], int]


class ControllerSystem(System):

    def initialize(self) -> None:
        self.input = self.engine[InputManager]
        self.query("controllers", all_of=[
            components.Controller,
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
        controllers = self._queries["controllers"].result

        speed = 200
        dt = self.engine[WindowManager].delta

        for entity in controllers:
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


class RenderSystem(System):

    def initialize(self) -> None:
        self.renderer = self.engine[RenderManager].renderer
        self.query("renderables", all_of=[
            components.Renderable,
            components.Position,
        ])

    def update(self) -> None:
        renderables = self._queries["renderables"].result
        for entity in renderables:
            renderable = entity[components.Renderable]
            position = entity[components.Position]

            if renderable.surface is None:
                continue

            renderable.update()

            self.renderer.blit(
                params={
                    "source": renderable.surface,
                    "position": (position.x, position.y),
                },
                z_level=107 if renderable.alpha else 1,
            )


def setup_player(ecs: pecs.Engine) -> pecs.Entity:
    player = ecs.entities.create("player")
    ecs.components.attach(player, components.Renderable, {
        "asset_path": Path("./tests/assets/animations/player"),
        "foreground": Color(255, 255, 255),
        "background": Color(0, 0, 0),
        "alpha": True,
        "scale": 4.0,
    })
    ecs.components.attach(player, components.Controller)
    ecs.components.attach(player, components.Position, {
        "x": 30,
        "y": 30,
    })
    return player


class ECSLoop(Loop):

    def initialize(self) -> None:
        self.render_system = RenderSystem(self.engine, self)
        self.controller_system = ControllerSystem(self.engine, self)

        setup_player(self.ecs)

    def teardown(self) -> None:
        pass

    def pre_update(self) -> None:
        self.last_pre_tick = time.time()

    def update(self) -> None:
        self.controller_system.update()
        self.render_system.update()
        self.tick()

    def post_update(self) -> None:
        self.last_post_tick = time.time()


class UILoop(Loop):

    def initialize(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def pre_update(self) -> None:
        pass

    def update(self) -> None:
        self.tick()

    def post_update(self) -> None:
        pass


class Game:

    def __init__(self) -> None:
        self.engine = Engine(
            config=Config(
                config_path=Path("./tests/")
            ),
            init_mapping={
                ECSManager.id: {
                    "loader": Loader(components),
                    "loop": ECSLoop,
                },
                UIManager.id: {
                    "loader": Loader(ui),
                    "loop": UILoop,
                }
            }
        )

    def start(self) -> None:
        self.engine.boot()


if __name__ == '__main__':
    game = Game()
    game.start()
