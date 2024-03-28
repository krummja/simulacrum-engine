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
from tests.game.ui.test_panels import setup_test_panels


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
        "scale": 4.0,
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
