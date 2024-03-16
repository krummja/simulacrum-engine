from pecs_framework import Loader, BaseSystem
import pecs_framework as pecs

from pathlib import Path
from rich import inspect

from simulacrum_engine.core import *
from simulacrum_engine.core.ecs.ecs_manager import Loop
from tests import components


class SimulacrumSystem(BaseSystem):

    def __init__(self, engine: Engine, loop: pecs.base_system.Loop) -> None:
        self.engine = engine
        super().__init__(loop)


class RenderSystem(SimulacrumSystem):

    def initialize(self):
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

        e1 = self.ecs.entities.create("e1")
        self.ecs.components.attach(e1, components.Renderable, {
            "asset_path": Path("./tests/assets/light.png"),
            "foreground": Color(255, 255, 255),
            "background": Color(0, 0, 0),
            "alpha": True,
        })

        self.ecs.components.attach(e1, components.Position, {
            "x": 10,
            "y": 10,
        })

    def teardown(self) -> None:
        pass

    def pre_update(self) -> None:
        pass

    def update(self) -> None:
        self.render_system.update()

    def post_update(self) -> None:
        pass


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
