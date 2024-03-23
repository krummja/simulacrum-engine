from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from pathlib import Path
import pygame as pyg
import pecs_framework as pecs

from simulacrum_engine.rendering.render_manager import RenderManager
from simulacrum_engine.window import WindowManager
from simulacrum_engine.ecs import ECSManager
from simulacrum_engine.component import EngineComponent
from simulacrum_engine.events import Events
from simulacrum_engine.ui.elements.text import UIText
from simulacrum_engine.ecs import Loop


class UIManager(EngineComponent):

    def boot(self, *, loader: pecs.Loader, loop: type[Loop]) -> bool:
        self.ecs = pecs.Engine(loader)
        self.ecs.create_domain("UI")
        self.ecs.components.load()
        self.loop = loop(self.engine, self.ecs, self.ecs.domain)

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
