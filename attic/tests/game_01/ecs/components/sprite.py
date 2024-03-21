from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import pygame as pyg
from dataclasses import dataclass
from pecs_framework import Component


@dataclass
class Sprite(Component):
    surface: pyg.Surface
