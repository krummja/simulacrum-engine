from __future__ import annotations

from dataclasses import dataclass
import pecs_framework as pecs
import math


@dataclass
class Velocity(pecs.Component):
    x: float = 0.0
    y: float = 0.0
    max_velocity: float = 100.0
    drag_rate: float = 10.0
