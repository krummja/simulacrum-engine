from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from pecs_framework import Loader

import time
from pathlib import Path
from simulacrum_engine import AssetManager
from simulacrum_engine import Engine
from simulacrum_engine import Config
from simulacrum_engine import ECSManager
from simulacrum_engine import RenderManager
from simulacrum_engine import UIManager
from simulacrum_engine.ecs.loop import Loop

from tests import components
from tests.game.controller import ControllerSystem
from tests.game.rendering import RenderSystem
from tests.game.physics import PhysicsSystem
from tests.game.ui.test_panels import setup_test_panels
from tests.game.player import setup_player


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

        setup_test_panels(self.engine[UIManager])

    def start(self) -> None:
        self.engine.boot()


if __name__ == '__main__':
    game = Game()
    game.start()
