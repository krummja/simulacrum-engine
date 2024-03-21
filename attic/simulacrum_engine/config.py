from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import re
import tomlkit as toml
import pygame as pyg
from pathlib import Path
from pydantic import BaseModel
from pydantic import field_validator


class WindowConfig(BaseModel):
    width: int = 1024
    height: int = 768
    title: str = ""
    icon_path: Path | str = ""
    fps_cap: int = 60
    render_scale: int | float = 1
    resizable: bool = False
    fullscreen: bool = False
    debug: bool = False


class ShaderConfig(BaseModel):
    opengl: bool = False
    fragment_path: Path | str = ""


class InputConfig(BaseModel):
    quit: str = "escape"


class ECSConfig(BaseModel):
    enable: bool = True
    component_path: Path | str = ""
    domain_id: str = ""


class Config:

    def __init__(self, config_path: Path | str, config_file: str) -> None:
        if isinstance(config_path, str):
            config_path = Path(config_path).resolve()
        self.config_path = config_path
        self.config_file = Path(self.config_path, config_file)

        if not self.config_file.exists():
            self.initialize()
            self.save()

        self.load()

    def initialize(self) -> None:
        self.window = WindowConfig()
        self.shader = ShaderConfig()
        self.input = InputConfig()
        self.ecs = ECSConfig()

    def save(self) -> None:
        document = toml.document()
        document.add(toml.nl())
        window = toml.table()
        shader = toml.table()
        input = toml.table()
        ecs = toml.table()

        for key, value in self.window.model_dump().items():
            window.add(key, value)
        document.add("window", window)

        for key, value in self.shader.model_dump().items():
            shader.add(key, value)
        document.add("shaders", shader)

        for key, value in self.input.model_dump().items():
            input.add(key, value)
        document.add("input", input)

        for key, value in self.ecs.model_dump().items():
            ecs.add(key, value)
        document.add("ecs", ecs)

        with open(self.config_file, "w+") as file:
            file.write(toml.dumps(document))

    def load(self) -> None:
        with open(self.config_file, "r") as file:
            self.config = toml.parse(file.read())
            self.window_opts = self.config["window"].unwrap()
            self.shader_opts = self.config["shaders"].unwrap()
            self.input_opts = self.config["input"].unwrap()
            self.ecs_opts = self.config["ecs"].unwrap()

        self.load_window()
        self.load_shader()
        self.load_input()
        self.load_ecs()

    def load_window(self) -> None:
        icon_path = self.window_opts["icon_path"]
        if icon_path != "":
            abs_icon_path = config_path_util(self.config_path, icon_path)
            self.window_opts["icon_path"] = abs_icon_path
        self.window = WindowConfig(**self.window_opts)

    def load_shader(self) -> None:
        frag_path = self.shader_opts["fragment_path"]
        if frag_path != "":
            abs_shader_path = config_path_util(self.config_path, frag_path)
            self.shader_opts["fragment_path"] = abs_shader_path
        self.shader = ShaderConfig(**self.shader_opts)

    def load_input(self) -> None:
        self.input = InputConfig(**self.input_opts)

    def load_ecs(self) -> None:
        component_path = self.ecs_opts["component_path"]
        if component_path != "":
            abs_component_path = config_path_util(self.config_path, component_path)
            self.ecs_opts["component_path"] = abs_component_path
        self.ecs = ECSConfig(**self.ecs_opts)


def config_path_util(start_from: Path, path: str) -> Path:
    path_parts = path.split("/")

    # Relative path from config directory
    if path_parts[0] == "..":
        path_parts[0] = str(start_from.parent)

    # Absolute path under arbitrary drive letter
    elif re.match(r"\w:", path_parts[0]):
        path_parts[0] = path_parts[0] + "/"

    return Path(*path_parts)
