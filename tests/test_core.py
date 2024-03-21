from pecs_framework import Loader, BaseSystem
import pecs_framework as pecs

import time
from pathlib import Path
from rich import inspect

import pygame as pyg
from simulacrum_engine.core import *
from simulacrum_engine.core.ecs import Loop
from simulacrum_engine.core.ecs import System
from tests import components


class ControllerSystem(System):

    def initialize(self) -> None:
        self.input = self.engine[InputManager]
        self.query("controllers", all_of=[
            components.Controller,
            components.Position,
        ])

    def update(self) -> None:
        controllers = self._queries["controllers"].result

        speed = 200
        dt = self.engine[WindowManager].delta

        for entity in controllers:
            position = entity[components.Position]
            input_vector = pyg.Vector2(0, 0)

            if self.input.keyboard.holding("W"):
                input_vector.y = -1
            if self.input.keyboard.holding("S"):
                input_vector.y = 1
            if self.input.keyboard.holding("A"):
                input_vector.x = -1
            if self.input.keyboard.holding("D"):
                input_vector.x = 1

            move_direction = pyg.Vector2(input_vector.x, input_vector.y)
            magnitude = move_direction.magnitude()

            if magnitude != 0:
                move_direction.normalize()

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


class ECSLoop(Loop):

    def initialize(self) -> None:
        self.render_system = RenderSystem(self.engine, self)
        self.controller_system = ControllerSystem(self.engine, self)

        player = self.ecs.entities.create("player")
        self.ecs.components.attach(player, components.Renderable, {
            "asset_path": Path("./tests/assets/textures/player/idle"),
            "foreground": Color(255, 255, 255),
            "background": Color(0, 0, 0),
            "alpha": True,
            "scale": 4.0,
        })
        self.ecs.components.attach(player, components.Controller)
        self.ecs.components.attach(player, components.Position, {
            "x": 30,
            "y": 30,
        })

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


class Game:

    def __init__(self) -> None:
        self.engine = Engine(
            init_mapping={
                ECSManager.id: {
                    "loader": Loader(components),
                    "loop": ECSLoop,
                }
            }
        )

    def start(self) -> None:
        self.engine.boot()


if __name__ == '__main__':
    game = Game()
    game.start()
