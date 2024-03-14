from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from pygame import Color as PGColor


class Color(PGColor):

    def to_tuple(self) -> tuple[int, ...]:
        return (self.r, self.g, self.b, self.a)

    def __hash__(self):
        return hash((self.r, self.g, self.b, self.a))
