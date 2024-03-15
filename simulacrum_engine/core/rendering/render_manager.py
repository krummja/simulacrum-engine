from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import pygame as pyg

from simulacrum_engine.core.logger import log_boot
from simulacrum_engine.core.component import EngineComponent
from simulacrum_engine.core.events import Events

from .renderer import Renderer


class RenderManager(EngineComponent):

    @log_boot
    def boot(self) -> bool:
        self.window_config = self.engine.config.window

        self.display_size = (
            self.window_config.width // self.window_config.render_scale,
            self.window_config.height // self.window_config.render_scale,
        )

        self._renderer = Renderer()

        # PyGame Surfaces that the renderer blits to.
        # In opengl mode, they act as a buffer that are then presented to the
        # gl_context
        self._uniforms = {
            "surface": pyg.Surface(self.display_size),
            "ui_surf": pyg.Surface(self.display_size, pyg.SRCALPHA),
        }

        self.emitter.on(Events.UPDATE, self.cycle)
        return True

    @property
    def uniforms(self) -> dict[str, pyg.Surface]:
        return self._uniforms

    def ready(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def cycle(self) -> None:
        self.uniforms["surface"].fill((21, 21, 21))
        self.uniforms["ui_surf"].fill((0, 0, 0, 0))
        self._renderer.cycle(self.uniforms)
