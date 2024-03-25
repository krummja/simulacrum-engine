from __future__ import annotations
from typing import *
from dataclasses import dataclass
from functools import cached_property
import pecs_framework as pecs

from pathlib import Path
import pygame as pyg


@dataclass
class Sprite(pecs.Component):
    texture: pyg.Surface

    def __post_init__(self) -> None:
        pass
