from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from pathlib import Path
from simulacrum_engine.utils import io_utils
from simulacrum_engine.assets.asset import Asset


def load_image_directory(path: Path):
    return io_utils.recursive_file_op(path, Asset, filetype="png")

