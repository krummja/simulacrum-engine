from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from simulacrum_engine.core.engine import Engine

import time
import pecs_framework as pecs

from collections import deque
from simulacrum_engine.core.component import EngineComponent
from simulacrum_engine.core.events import Events


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


class System(pecs.BaseSystem):

    def __init__(self, engine: Engine, loop: pecs.base_system.Loop) -> None:
        self.engine = engine
        super().__init__(loop)


class ECSManager(EngineComponent):

    def boot(
        self,
        *,
        loader: pecs.Loader,
        loop: type[Loop],
    ) -> bool:
        self.ecs = pecs.Engine(loader)
        self.ecs.create_domain(self.engine.config.ecs.domain_id)
        self.ecs.components.load()
        self.loop = loop(self.engine, self.ecs, self.ecs.domain)

        self.emitter.on(Events.PRE_UPDATE, self.pre_update)
        self.emitter.on(Events.UPDATE, self.cycle)
        self.emitter.on(Events.POST_UPDATE, self.post_update)
        return True

    def ready(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def pre_update(self) -> None:
        self.loop.pre_update()

    def cycle(self) -> None:
        self.loop.update()

    def post_update(self) -> None:
        self.loop.post_update()
