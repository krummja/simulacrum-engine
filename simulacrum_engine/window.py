from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import time
import pygame as pyg
from pathlib import Path
from simulacrum_engine.input import Input
from simulacrum_engine.shaderlib import MGL


ColorValue = pyg.Color | int | str | tuple[int, int, int] | Sequence[int]


class Window:

    def __init__(
        self,
        *,
        dimensions: tuple[int, int],
        title: str = "",
        flags: int = 0,
        fps_cap: int = 60,
        dt: int = 1,
        opengl: bool = False,
        frag_path: Path | None = None,
    ) -> None:
        self.dimensions = dimensions
        self.title = title
        self.flags = flags
        self.fps_cap = fps_cap
        self.dt = dt
        self.opengl = opengl
        self.frag_path = frag_path

        if self.opengl:
            self.flags = self.flags | pyg.DOUBLEBUF | pyg.OPENGL

        self.background_color = (21, 21, 21)

        self.time = time.time()
        self.start_time = time.time()
        self.frames = 0
        self.frame_log = []

        pyg.init()
        pyg.display.set_caption(title)

        self.input: Input | None = None
        self.screen = pyg.display.set_mode(self.dimensions, self.flags)
        self.clock = pyg.time.Clock()

        self.last_frame = time.time()
        self.dt = 0.1

        self.render_object = None
        if opengl:
            self.mgl = MGL()
            if self.frag_path is None:
                self.render_object = self.mgl.default_render_object()
            else:
                self.render_object = self.mgl.render_object(self.frag_path)

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
