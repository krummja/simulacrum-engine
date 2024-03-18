from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from simulacrum_engine.core.rendering.render_object import RenderObject

import time
import pygame as pyg

from simulacrum_engine.core.config import WindowConfig
from simulacrum_engine.core.config import ShaderConfig
from simulacrum_engine.core.rendering.gl_context import GLContext


class FrameManager:

    def __init__(self, window: Window) -> None:
        self.window = window
        self.time = time.time()
        self.clock = pyg.time.Clock()

        self.frames = 0
        self.frame_log = [0.1]
        self.last_frame = time.time()
        self.frame_delta = 0.1

    @property
    def fps(self) -> float:
        return len(self.frame_log) / sum(self.frame_log)

    def cycle(self) -> None:
        self.clock.tick(self.window.fps_cap)
        self.frame_delta = min(time.time() - self.last_frame, self.frame_delta)
        self.frame_log.append(self.frame_delta)
        self.frame_log = self.frame_log[-60:]
        self.last_frame = time.time()

    def next_frame(self) -> None:
        self.time = time.time()
        self.frames += 1


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


class Window:
    """
    Window object wrapping the FrameManager and Screen.
    In opengl mode, the Screen passes its internal PyGame display as the RenderObject
    surface.
    """

    def __init__(
        self,
        window: WindowConfig,
        shader: ShaderConfig,
    ) -> None:
        self.dimensions = (window.width, window.height)
        self.title = window.title
        self.icon_path = window.icon_path
        self.flags = pyg.RESIZABLE if window.resizable else 0
        self.fps_cap = window.fps_cap

        self.opengl = shader.opengl
        self.fragment_path = shader.fragment_path

        if self.opengl:
            self.flags = self.flags | pyg.DOUBLEBUF | pyg.OPENGL

        self.background_color = (21, 21, 21)

        self.frame_manager = FrameManager(self)
        self.screen = Screen(self)

        if window.icon_path:
            icon = pyg.image.load(window.icon_path).convert_alpha()
            pyg.display.set_icon(icon)

    def cycle(self, uniforms: dict[str, Any] | None = None) -> None:
        self.screen.cycle(uniforms)
        self.frame_manager.cycle()

        self.screen.clear()
        self.frame_manager.next_frame()
