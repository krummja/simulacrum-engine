from __future__ import annotations
from dataclasses import dataclass
import pecs_framework as pecs


@dataclass
class Position(pecs.Component):
    x: float
    y: float
