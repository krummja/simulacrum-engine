from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from simulacrum_engine.core.window.window import Window

import pygame as pyg
import time


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
