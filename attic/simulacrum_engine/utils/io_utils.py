from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import os
import json
from pathlib import Path


def read_json(path: str | Path) -> dict[str, Any]:
    file = open(path, "r")
    data = json.load(file)
    file.close()
    return data


class ResolverFunction(Protocol):
    def __call__(self, path: Path) -> Any:
        ...


def recursive_file_op(
    path: Path,
    resolver_func: ResolverFunction,
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
