from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from simulacrum_engine.logger import log_boot
from simulacrum_engine.component import EngineComponent
from simulacrum_engine.rendering.render_manager import RenderManager
from simulacrum_engine.events import Events

from .window import Window


class WindowManager(EngineComponent):

    def boot(self) -> bool:
        self.window = Window(
            self.engine.config.window,
            self.engine.config.shader,
        )

        self.emitter.on(Events.POST_UPDATE, self.cycle)
        self.uniforms = self.engine[RenderManager].uniforms
        return True

    def cycle(self) -> None:
        self.window.cycle({
            "surface": self.uniforms["default"],
            "ui_surf": self.uniforms["ui_surf"],
        })

    @property
    def delta(self) -> float:
        return self.window.frame_manager.frame_delta

    @property
    def fps(self) -> float:
        return self.window.frame_manager.fps
