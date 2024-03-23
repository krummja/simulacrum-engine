from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from pygame import Color as PGColor


class Color(PGColor):

    @staticmethod
    def from_pyg(color: PGColor) -> Color:
        return Color(color.r, color.g, color.b, color.a)

    def to_tuple(self) -> tuple[int, ...]:
        return (self.r, self.g, self.b, self.a)

    def __hash__(self):
        return hash((self.r, self.g, self.b, self.a))

    def as_pyg(self) -> PGColor:
        return PGColor(self.r, self.g, self.b, self.a)
