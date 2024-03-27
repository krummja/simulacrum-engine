from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import pecs_framework as pecs
from pecs_framework import Loader

import time
from pathlib import Path
from simulacrum_engine import *
from simulacrum_engine.ecs.loop import Loop
from simulacrum_engine.ui.elements.panel import Panel

from tests import components
from tests.game.controller import ControllerSystem
from tests.game.rendering import RenderSystem
from tests.game.physics import PhysicsSystem


class PlayerModel:

    def __init__(self, entity: pecs.Entity) -> None:
        self.entity = entity
        self.animatable = entity[components.Animatable]

    def animate_stop(self) -> None:
        self.animatable.set_animation("idle")

    def animate_move(self) -> None:
        self.animatable.set_animation("run")


def setup_player(assets: AssetManager, ecs: pecs.Engine) -> pecs.Entity:
    player = ecs.entities.create("player")

    assets.try_load(AssetType.ANIMATION, "player")
    animations = assets.get_assets_for(AssetType.ANIMATION, "player")

    ecs.components.attach(player, components.Animatable, {
        "animations": animations,
        "start_animation": "idle",
    })

    ecs.components.attach(player, components.Renderable, {
        "foreground": Color(255, 255, 255),
        "background": Color(0, 0, 0),
        "alpha": True,
        "scale": 10.0,
    })

    ecs.components.attach(player, components.Controllable)

    ecs.components.attach(player, components.Position, {
        "x": 600,
        "y": 150,
    })

    ecs.components.attach(player, components.Velocity)

    ecs.components.attach(player, components.StateControl, {
        "state_model": PlayerModel(player),
        "states": [
            {"name": "idle", "on_enter": ["animate_stop"]},
            {"name": "move", "children": [
                {"name": "up", "on_enter": ["animate_move"]},
                {"name": "left", "on_enter": ["animate_move"]},
                {"name": "down", "on_enter": ["animate_move"]},
                {"name": "right", "on_enter": ["animate_move"]},
            ]}
        ],
        "initial": "idle",
    })

    return player


class ECSLoop(Loop):

    def initialize(self) -> None:
        self.render_system = RenderSystem(self.engine, self)
        self.controller_system = ControllerSystem(self.engine, self)
        self.physics_system = PhysicsSystem(self.engine, self)

        setup_player(self.engine[AssetManager], self.ecs)

    def teardown(self) -> None:
        pass

    def pre_update(self) -> None:
        self.last_pre_tick = time.time()
        self.physics_system.update()

    def update(self) -> None:
        self.controller_system.update()
        self.render_system.update()
        self.tick()

    def post_update(self) -> None:
        self.last_post_tick = time.time()


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
            }
        )

        self.engine[RenderManager].renderer.set_groups(["default", "ui"])
        self.engine[UIManager].add_element("panel", Panel, {
            "x": 10,
            "y": 10,
            "width": 200,
            "height": 400,
            "background": Color(55, 55, 55),
            "on_mouse_enter": (lambda event: print(event)),
            "on_mouse_leave": (lambda event: print(event)),
        })

    def start(self) -> None:
        self.engine.boot()


if __name__ == '__main__':
    game = Game()
    game.start()
