from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from pathlib import Path
import math
import random

import pygame as pyg
from pygame.locals import *

import pecs_framework as pecs

import simulacrum_engine as siml
from simulacrum_engine.renderer import Position
from simulacrum_engine.ui_lib.text import UIText

from ecs.systems.render_system import RenderSystem


TEST_DIR = Path(__file__).parent.resolve()
SHADER_DIR = Path(TEST_DIR, "shaders")
CONFIG_DIR = Path(TEST_DIR, "config")
TEXTURE_DIR = Path(TEST_DIR, "textures")
FONT_DIR = Path(TEST_DIR, "fonts")


def advance(vec, angle, amt):
    vec[0] += math.cos(angle) * amt
    vec[1] += math.sin(angle) * amt
    return vec


def load_png(filename: str) -> tuple[pyg.Surface, pyg.Rect]:
    path = Path(TEXTURE_DIR, filename)
    try:
        image = pyg.image.load(path)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Image {filename} not found")
        raise SystemExit
    return image, image.get_rect()


class Loop(siml.Loop):

    def initialize(self) -> None:
        self.render_system = RenderSystem(self)

    def teardown(self) -> None:
        pass

    def pre_update(self) -> None:
        pass

    def update(self) -> None:
        self.render_system.update()

    def post_update(self) -> None:
        pass


class Game(siml.Game):

    def load(self) -> None:
        self.text = UIText(FONT_DIR)
        self.camera = siml.Camera(self.display.get_size(), drag=1)
        # self.prepare_background()

    # def prepare_background(self) -> None:
    #     self.glow_img = pyg.Surface((255, 255))
    #     self.glow_img.fill((round(174 * 0.2), round(266 * 0.2), round(255 * 0.3)))

    #     glow_img, _ = load_png("light.png")
    #     self.glow_img.blit(
    #         glow_img,
    #         (0, 0),
    #         special_flags=pyg.BLEND_RGBA_MULT,
    #     )

    #     self.fireflies = []
    #     for _ in range(300):
    #         self.fireflies.append([
    #             [
    #                 random.random() * self.display.get_width(),
    #                 random.random() * self.display.get_height(),
    #             ],
    #             random.random() * math.pi * 2,
    #             random.random() * 10 + 10,
    #             random.random() * 4 * random.choice([-1, 1]),
    #         ])

    #     self.firefly_img = pyg.Surface((1, 1))
    #     self.firefly_img.fill((255, 255, 255))

    # def render_background(self) -> None:
    #     for firefly in self.fireflies:
    #         firefly[0] = advance(firefly[0], firefly[1], firefly[2] * self.window.dt)
    #         firefly[1] += firefly[3] * self.window.dt

    #         if random.random() * 4 < self.window.dt:
    #             firefly[3] = random.random() * 4 * random.choice([-1, 1])
    #             firefly[2] = random.random() * 10 + 10

    #         wpos = (
    #             int(firefly[0][0] % self.display.get_width()),
    #             int(firefly[0][1] % self.display.get_height()),
    #         )

    #         self.renderer.blit({
    #             "source": self.firefly_img,
    #             "position": Position(wpos[0], wpos[1]),
    #         }, z_level=11)

    #         diameter = math.sin(firefly[2] * 0.2 + self.window.time) * 8 + 25
    #         glow_img = pyg.transform.scale(self.glow_img, (diameter, diameter))

    #         self.renderer.blit({
    #             "source": glow_img,
    #             "position": Position(
    #                 (wpos[0] - glow_img.get_width() // 2),
    #                 (wpos[1] - glow_img.get_height() // 2),
    #             ),
    #         }, z_level=107)

    def render_debug(self) -> None:
        self.text["small_font"].render_with(self.renderer, {
            "text": f"FPS: {round(self.window.fps)}",
            "loc": (8, 8),
        })

    def update(self) -> None:
        self.display.fill((21, 21, 21))
        self.ui_surf.fill((0, 0, 0, 0))

        self.camera.update(self.window.dt)

        # self.render_background()
        self.render_debug()

        self.renderer.cycle({
            "default": self.display,
            "ui": self.ui_surf,
        })

        self.window.cycle({
            "surface": self.display,
            "ui_surf": self.ui_surf,
        })


def main() -> None:
    game = Game(CONFIG_DIR, "test.toml", loop=Loop)
    game.run()


if __name__ == '__main__':
    main()
