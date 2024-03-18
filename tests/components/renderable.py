from __future__ import annotations
from dataclasses import dataclass
from functools import cached_property
import pecs_framework as pecs

from pathlib import Path
import pygame as pyg

from simulacrum_engine.core.rendering.color import Color
from simulacrum_engine.core.assets.asset_utils import load_image


@dataclass
class Renderable(pecs.Component):
    asset_path: Path
    foreground: Color
    background: Color
    alpha: bool = False
    scale: float = 1.0

    @cached_property
    def surface(self) -> pyg.Surface:
        return pyg.Surface((255 * self.scale, 255 * self.scale))

    def __post_init__(self) -> None:
        asset = load_image(self.asset_path, alpha=True)
        asset = pyg.transform.scale(asset, (
            asset.get_width() * self.scale,
            asset.get_height() * self.scale,
        ))

        flags = pyg.BLEND_RGBA_MULT if self.alpha else 0
        self.surface.fill(self.foreground)
        self.surface.blit(asset, (0, 0), special_flags=flags)
