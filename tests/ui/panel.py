from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from pathlib import Path
from dataclasses import dataclass
import pecs_framework as pecs

from simulacrum_engine import Color


@dataclass
class Panel(pecs.Component):
    background_path: Path | None = None
    background_color: Color | None = None
    padding_top: int = 0
    padding_right: int = 0
    padding_bottom: int = 0
    padding_left: int = 0
