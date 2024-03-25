from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import pygame as pyg

from simulacrum_engine.component import EngineComponent
from simulacrum_engine.events import Events

from .renderer import Renderer


class RenderManager(EngineComponent):

    def boot(self) -> bool:
        self.window_config = self.engine.config.window

        self.display_size = (
            self.window_config.width // self.window_config.render_scale,
            self.window_config.height // self.window_config.render_scale,
        )

        self._renderer = Renderer()

        # PyGame Surfaces that the renderer blits to.
        # In opengl mode, they act as a buffer that are then presented to the gl_context
        self._uniforms = {
            "default": pyg.Surface(self.display_size),
            "ui_surf": pyg.Surface(self.display_size, pyg.SRCALPHA),
        }

        self.emitter.on(Events.UPDATE, self.cycle)
        return True

    @property
    def renderer(self) -> Renderer:
        return self._renderer

    @property
    def uniforms(self) -> dict[str, pyg.Surface]:
        return self._uniforms

    def ready(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def cycle(self) -> None:
        self.uniforms["default"].fill((21, 21, 21))

        # ! In order to use the UI Surface like this, I need a key color
        self.uniforms["ui_surf"].fill((0, 0, 0, 0))
        self._renderer.cycle(dest_surfaces=self.uniforms)
