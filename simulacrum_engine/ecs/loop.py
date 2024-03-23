from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from simulacrum_engine.engine import Engine

import time

import pecs_framework as pecs



class Loop(pecs.base_system.Loop):

    def __init__(self, engine: Engine, ecs: pecs.Engine, domain: pecs.Domain) -> None:
        self.engine = engine

        self.last_pre_tick = time.time()
        self.last_post_tick = time.time()

        self.ticks = 0
        self.last_tick = time.time()
        self.tick_delta = 0

        super().__init__(ecs, domain)

    @property
    def tps(self) -> float:
        return 0.0

    def tick(self) -> None:
        self.last_tick = time.time()
        self.ticks += 1
