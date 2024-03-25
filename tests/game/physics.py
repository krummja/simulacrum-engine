from __future__ import annotations
from typing import *

from simulacrum_engine import *
from simulacrum_engine.ecs.system import System

from tests import components


class PhysicsSystem(System):

    def initialize(self) -> None:
        self.physics = self.engine[PhysicsManager]
        self.query("bodies", all_of=[
            components.PhysicsBody,
            components.Velocity,
        ])

    def update(self) -> None:
        bodies = self._queries["bodies"].result
        for entity in bodies:
            body = entity[components.PhysicsBody]
            if not body.is_added:
                self.physics.add_body(body.add())
