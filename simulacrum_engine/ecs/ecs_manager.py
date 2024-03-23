from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import pecs_framework as pecs

from simulacrum_engine.ecs.loop import Loop
from simulacrum_engine.component import EngineComponent
from simulacrum_engine.events import Events


class ECSManager(EngineComponent):

    def boot(self, *, loader: pecs.Loader, loop: type[Loop]) -> bool:
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
