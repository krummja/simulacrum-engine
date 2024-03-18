from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from pathlib import Path
import pygame as pyg

from simulacrum_engine.core.rendering.render_manager import RenderManager
from simulacrum_engine.core.window import WindowManager
from simulacrum_engine.core.ecs import ECSManager
from simulacrum_engine.core.component import EngineComponent
from simulacrum_engine.core.events import Events
from simulacrum_engine.core.ui.elements.text import UIText


class UIManager(EngineComponent):

    def boot(self) -> bool:
        self.config = self.engine.config.asset
        self.renderer = self.engine[RenderManager].renderer
        self.text = UIText(Path(self.config.asset_path, "fonts"))
        self.emitter.on(Events.UPDATE, self.cycle)
        return True

    def cycle(self) -> None:
        if self.engine.config.window.debug:
            fps = self.engine[WindowManager].fps
            ticks = self.engine[ECSManager].loop.ticks

            self.text["large_font"].render_with(self.renderer, {
                "text": f"FPS: {round(fps)}",
                "loc": (8, 8 * 1),
            })

            self.text["large_font"].render_with(self.renderer, {
                "text": f"TCK: {round(ticks)}",
                "loc": (8, 8 * 4),
            })
