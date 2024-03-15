from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from simulacrum_engine.core.logger import log_boot
from simulacrum_engine.core.component import EngineComponent
from simulacrum_engine.core.rendering.render_manager import RenderManager
from simulacrum_engine.core.events import Events

from .window import Window


class WindowManager(EngineComponent):

    @log_boot
    def boot(self) -> bool:
        self.window = Window(
            self.engine.config.window,
            self.engine.config.shader,
        )

        self.emitter.on(Events.POST_UPDATE, self.cycle)
        self.uniforms = self.engine[RenderManager].uniforms
        return True

    def ready(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def cycle(self) -> None:
        self.window.cycle({
            "surface": self.uniforms["surface"],
            "ui_surf": self.uniforms["ui_surf"],
        })
