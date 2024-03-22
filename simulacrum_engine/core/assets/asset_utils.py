from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import os
import pygame as pyg
from pathlib import Path

from simulacrum_engine.core.rendering.color import Color
from devtools import debug


T = TypeVar("T", covariant=True)


class ResolverFunction(Protocol, Generic[T]):
    def __call__(self, path: Path) -> T:
        ...

class ResolvedAsset(NamedTuple, Generic[T]):
    key: str
    value: T
    level: int


def unnest_recursed(
    assets: dict[str, Any],
    unnested: list[ResolvedAsset[Any]],
    level: int = 0,
) -> dict[str, list[ResolvedAsset[Any]]]:
    unnested_map = {}

    for k, v in assets.items():
        if not isinstance(v, dict):
            unnested.append(ResolvedAsset(k, v, level))
        else:
            level += 1
            unnested_map = {f"{k}/{_k}": _v for _k, _v in v.items()}
            unnest_recursed(v, unnested, level)

    return unnested_map


def recursive_file_op(
    path: Path,
    resolver_func: ResolverFunction[T],
    *,
    filetype: str | None = None
) -> dict[str, list[ResolvedAsset[T]]]:
    data = {}
    out_data = []
    base_path = path.parts

    for file in os.walk(path):
        wpath = file[0].replace("\\", "/").split("/")
        path_ref = wpath.copy()
        data_ref = data

        while len(path_ref) > len(base_path):
            current_dir = path_ref[len(base_path)]
            if current_dir not in data_ref:
                data_ref[current_dir] = {}
            data_ref = data_ref[current_dir]
            path_ref.pop(len(base_path))

        for asset in file[2]:
            asset_type = asset.split(".")[-1]
            if (asset_type == filetype) or (filetype is None):
                data_ref[asset.split(".")[0]] = resolver_func(Path(file[0], asset))

    return unnest_recursed(data, out_data)


def load_image(path: Path, alpha: bool = False, colorkey=None) -> pyg.Surface:
    if alpha:
        image = pyg.image.load(path).convert_alpha()
    else:
        image = pyg.image.load(path).convert()
    if colorkey:
        image.set_colorkey(colorkey)
    return image


def load_image_directory(
    path: Path,
    alpha: bool = False,
    colorkey: Color | None = None,
) -> dict[str, list[ResolvedAsset[pyg.Surface]]]:
    loaded = recursive_file_op(
        path,
        (lambda path: load_image(path, alpha, colorkey)),
        filetype="png",
    )

    debug(loaded)
    return loaded
