from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from simulacrum_engine.utils import gfx_utils


class Camera:

    def __init__(
        self,
        size: tuple[int, int],
        pos: tuple[float, float] = (0.0, 0.0),
        drag: int = 1,
    ) -> None:
        self.size = size
        self.pos = list(pos)
        self.int_pos = (int(pos[0]), int(pos[1]))
        self.drag = drag

    @property
    def target(self) -> tuple[float, float]:
        return (
            self._target[0] - self.size[0] // 2,
            self._target[1] - self.size[1] // 2,
        )

    @target.setter
    def target(self, value: tuple[float, float]) -> None:
        self._target = value

    def __iter__(self) -> Iterable[int]:
        for v in self.int_pos:
            yield v

    def __getitem__(self, item: int) -> int:
        return self.int_pos[item]

    def move(self, movement: tuple[float, float]) -> None:
        self.pos[0] += movement[0]
        self.pos[1] += movement[1]

    def update(self, dt: float) -> None:
        if self.target:
            self.pos[0] = gfx_utils.ease_approach(
                dt,
                self.pos[0],
                self.target[0],
                drag=self.drag,
            )

            self.pos[1] = gfx_utils.ease_approach(
                dt,
                self.pos[1],
                self.target[1],
                drag=self.drag,
            )

        self.int_pos = (int(self.pos[0]), int(self.pos[1]))
