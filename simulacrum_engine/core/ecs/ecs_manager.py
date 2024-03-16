from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from simulacrum_engine.core.engine import Engine

import pecs_framework as pecs

from simulacrum_engine.core.component import EngineComponent
from simulacrum_engine.core.events import Events


class Loop(pecs.base_system.Loop):

    def __init__(self, engine: Engine, ecs: pecs.Engine, domain: pecs.Domain) -> None:
        self.engine = engine
        super().__init__(ecs, domain)


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
        self.loop = loop(self.engine, self.ecs, self.ecs.domain)

        self.emitter.on(Events.PRE_UPDATE, self.cycle)
        return True

    def ready(self) -> None:
        self.ecs.components.load()

    def teardown(self) -> None:
        pass

    def cycle(self) -> None:
        self.loop.update()
