from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import os
import pygame as pyg
from pathlib import Path


def recursive_file_op(
    path: Path,
    resolver_func: Callable[[Path], Any],
    *,
    filetype: str | None = None
) -> dict[str, Any]:
    data = {}
    base_path = path.parts

    for f in os.walk(path):
        wpath = f[0].replace("\\", "/").split("/")
        path_ref = wpath.copy()
        data_ref = data

        while len(path_ref) > len(base_path):
            current_dir = path_ref[len(base_path)]
            if current_dir not in data_ref:
                data_ref[current_dir] = {}
            data_ref = data_ref[current_dir]
            path_ref.pop(len(base_path))

        for asset in f[2]:
            asset_type = asset.split(".")[-1]
            if (asset_type == filetype) or (filetype is None):
                data_ref[asset.split(".")[0]] = resolver_func(Path(f[0], asset))

    return data


def load_image(path: Path, alpha: bool = False, colorkey=None):
    if alpha:
        image = pyg.image.load(path).convert_alpha()
    else:
        image = pyg.image.load(path).convert()
    if colorkey:
        image.set_colorkey(colorkey)
    return image


def load_image_directory(path: Path, alpha: bool = False, colorkey=None):
    return recursive_file_op(
        path,
        lambda path: load_image(path, alpha, colorkey),
        filetype="png",
    )