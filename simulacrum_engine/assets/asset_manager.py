from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import time
import json

import pygame as pyg
from pathlib import Path
from simulacrum_engine.animation import Animation
from simulacrum_engine.animation import AnimationConfig
from simulacrum_engine.animation import DEFAULT_ANIMATION_CONFIG
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

                config_mapping: dict[str, AnimationConfig] = {}
                if (config_path := Path(subpath, "config.json")).exists():
                    with open(config_path, "r") as config_file:
                        config_mapping = json.loads(config_file.read())

                for animation_path in subpath.iterdir():
                    if asset := self.try_load_animation(animation_path, config_mapping):
                        if entity not in self.assets[AssetType.ANIMATION]:
                            self.assets[AssetType.ANIMATION][entity] = {}
                        self.assets[AssetType.ANIMATION][entity][asset.name] = asset

    def try_load_animation(
        self,
        path: Path,
        config_mapping: dict[str, AnimationConfig],
    ) -> Asset[Animation] | None:
        frames = []
        if path.exists() and path.is_dir():
            animation_name = path.name
            for image in path.iterdir():
                frame = pyg.image.load(image)
                frames.append(frame)
            config = config_mapping.get(animation_name, DEFAULT_ANIMATION_CONFIG)

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
