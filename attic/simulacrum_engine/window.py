from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import time
import pygame as pyg
from pathlib import Path
from simulacrum_engine.input import Input
from simulacrum_engine.shaderlib import MGL

from simulacrum_engine.config import WindowConfig
from simulacrum_engine.config import ShaderConfig


class Window:

    def __init__(self, window: WindowConfig, shader: ShaderConfig) -> None:
        self.dimensions = (window.width, window.height)
        self.title = window.title
        self.flags = pyg.RESIZABLE if window.resizable else 0
        self.fps_cap = window.fps_cap
        self.opengl = shader.opengl
        self.frag_path = shader.fragment_path

        if self.opengl:
            self.flags = self.flags | pyg.DOUBLEBUF | pyg.OPENGL

        self.background_color = (21, 21, 21)

        self.time = time.time()
        self.start_time = time.time()
        self.frames = 0
        self.frame_log = [0.1]

        pyg.init()
        pyg.display.set_caption(self.title)

        self.screen = pyg.display.set_mode(self.dimensions, self.flags)
        if window.icon_path:
            icon = pyg.image.load(window.icon_path).convert_alpha()
            pyg.display.set_icon(icon)

        self.clock = pyg.time.Clock()
        self.last_frame = time.time()
        self.dt = 0.1

        self.input: Input | None = None

        self.render_object = None
        if self.opengl:
            self.mgl = MGL()
            if self.frag_path is None:
                self.render_object = self.mgl.default_render_object()
            else:
                self.render_object = self.mgl.render_object(str(self.frag_path))

    @property
    def fps(self) -> float:
        return len(self.frame_log) / sum(self.frame_log)

    @property
    def runtime(self) -> float:
        return self.time - self.start_time

    def bind_input(self, input: Input) -> None:
        self.input = input

    def cycle(self, uniforms: dict[str, Any] | None = None) -> None:
        if uniforms is None:
            uniforms = {}

        if self.render_object is not None:
            if self.render_object.use_default and ("surface" not in uniforms):
                uniforms["surface"] = self.screen
            self.render_object.render(uniforms=uniforms)
        else:
            self.screen.blit(uniforms["default"], (0, 0))
            self.screen.blit(uniforms["ui"], (0, 0))

        pyg.display.flip()

        self.clock.tick(self.fps_cap)
        self.dt = min(time.time() - self.last_frame, self.dt)
        self.frame_log.append(self.dt)
        self.frame_log = self.frame_log[-60:]

        self.last_frame = time.time()

        self.screen.fill(self.background_color)

        if self.render_object:
            self.mgl.ctx.clear(
                *[self.background_color[i] / 255 for i in range(3)],
                alpha=1.0,
            )

        if self.input:
            self.input.update()

        self.time = time.time()
        self.frames += 1
