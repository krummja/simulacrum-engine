from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import time

import pygame as pyg
from pathlib import Path
from simulacrum_engine.animation import Animation, AnimationConfig
from simulacrum_engine.component import EngineComponent
from simulacrum_engine.events import Events
from simulacrum_engine.assets import asset_utils

from .asset import Asset, AT, _AssetType
from .asset import AssetType


AssetMap: TypeAlias = dict[AssetType, dict[str, dict[str, Asset[AT]]]]


class AssetManager(EngineComponent):

    def boot(self) -> bool:
        self.config = self.engine.config.asset
        self.asset_path = self.config.asset_path

        self.assets: AssetMap = {
            AssetType.ANIMATION: {},
            AssetType.AUDIO: {},
            AssetType.FONT: {},
            AssetType.SPRITESHEET: {},
            AssetType.TEXTURE: {},
        }

        return True

    def cycle(self) -> None:
        pass

    def try_load(self, asset_type: AssetType, entity: str) -> None:
        match asset_type:
            case AssetType.ANIMATION:
                subpath = Path(self.asset_path, "animations", entity)
                for animation_path in subpath.iterdir():
                    if asset := self.try_load_animation(animation_path, {
                        "frame_delay": 30,
                    }):
                        if entity not in self.assets[AssetType.ANIMATION]:
                            self.assets[AssetType.ANIMATION][entity] = {}
                        self.assets[AssetType.ANIMATION][entity][asset.name] = asset

    def try_load_animation(
        self,
        path: Path,
        config: AnimationConfig,
    ) -> Asset[Animation] | None:
        frames = []
        if path.exists():
            animation_name = path.name
            for image in path.iterdir():
                frame = pyg.image.load(image)
                frames.append(frame)
        animation = Animation(animation_name, frames, config)
        return Asset(animation_name, path, AssetType.ANIMATION, animation)

    def get_assets_for(
        self,
        asset_type: AssetType,
        entity: str,
    ) -> dict[str, Asset[_AssetType]]:
        match asset_type:
            case AssetType.ANIMATION:
                return self.assets[asset_type][entity]
            case _:
                return {}
