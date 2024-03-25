from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import pymunk as pym

from simulacrum_engine.window import WindowManager
from simulacrum_engine.component import EngineComponent
from simulacrum_engine.events import Events


class PhysicsManager(EngineComponent):

    def boot(self) -> bool:
        self.pixels_per_frame = 2
        self.speed = 0

        self.space = pym.Space()
        self.gravity = (0, -981)
        self.space.gravity = self.gravity

        self.physics_steps = 10

        self.emitter.on(Events.UPDATE, self.cycle)
        return True

    def ready(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def cycle(self) -> None:
        self.calculate_speed()
        for _ in range(self.physics_steps):
            self.space.step(self.speed / self.physics_steps)

    def calculate_speed(self) -> None:
        fps = self.engine[WindowManager].fps
        self.speed = self.pixels_per_frame / fps

    def add_body(self, body: pym.Body) -> None:
        self.space.add(body)
