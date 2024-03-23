from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from dataclasses import dataclass
import pecs_framework as pecs


@dataclass
class Rect(pecs.Component):
    x: int
    y: int
    width: int
    height: int
