from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from simulacrum_engine.core.window.window import Window
    from simulacrum_engine.core.rendering.render_object import RenderObject

from simulacrum_engine.core.rendering.gl_context import GLContext

import pygame as pyg


class Screen:

    def __init__(self, window: Window) -> None:
        self.window = window

        pyg.init()
        pyg.display.set_caption(window.title)
        self._screen = pyg.display.set_mode(window.dimensions, window.flags)

        self.render_object: RenderObject | None = None
        if window.opengl:
            self.gl_context = GLContext()
            if self.window.fragment_path is None:
                self.render_object = self.gl_context.default_render_object()
            else:
                self.render_object = self.gl_context.render_object(
                    fragment_path=str(self.window.fragment_path),
                )

    def cycle(self, uniforms: dict[str, Any] | None = None) -> None:
        if uniforms is None:
            uniforms = {}

        if self.render_object is not None:
            if self.render_object.use_default and ("surface" not in uniforms):
                uniforms["surface"] = self._screen
            self.render_object.render(uniforms=uniforms)
        else:
            self._screen.blit(uniforms["default"], (0, 0))
            self._screen.blit(uniforms["ui"], (0, 0))

        pyg.display.flip()

    def clear(self) -> None:
        if self.render_object:
            self.gl_context.ctx.clear(
                *[self.window.background_color[i] / 255 for i in range(3)],
                alpha=1.0,
            )

    def unwrap(self) -> pyg.Surface:
        return self._screen
