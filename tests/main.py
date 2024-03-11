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


class Game(siml.Game):

    def __init__(
        self,
        width: int = 960,
        height: int = 630,
        scale: int = 1,
        resizable: bool = False,
    ) -> None:
        self.width = width
        self.height = height
        self.scale = scale
        self.resizable = pyg.RESIZABLE if resizable else 0

    def load(self) -> None:

        self.window = siml.Window(
            dimensions=(self.width, self.height),
            title="Test Title",
            flags=self.resizable,
            opengl=True,
            fps_cap=60,
            frag_path=Path(SHADER_DIR, "frag.frag"),
        )

        self.input = siml.Input(Path(CONFIG_DIR, "config.json"))
        self.window.bind_input(self.input)

        self.renderer = siml.Renderer()
        self.renderer.set_groups(["ui", "default"])

        display_size = (self.width // self.scale, self.height // self.scale)
        self.display = pyg.Surface(display_size)
        self.ui_surf = pyg.Surface(display_size, pyg.SRCALPHA)

        self.text = UIText(FONT_DIR)

        self.glow_img = pyg.Surface((255, 255))
        self.glow_img.fill((round(174 * 0.2), round(266 * 0.2), round(255 * 0.3)))

        glow_img, glow_rect = load_png("light.png")
        self.glow_img.blit(
            glow_img,
            (0, 0),
            special_flags=pyg.BLEND_RGBA_MULT,
        )

        self.fireflies = []
        for _ in range(200):
            self.fireflies.append([
                [
                    random.random() * self.display.get_width(),
                    random.random() * self.display.get_height(),
                ],
                random.random() * math.pi * 2,
                random.random() * 10 + 10,
                random.random() * 4 * random.choice([-1, 1]),
            ])

        self.firefly_img = pyg.Surface((1, 1))
        self.firefly_img.fill((255, 255, 255))

    def render_background(self) -> None:
        for firefly in self.fireflies:
            firefly[0] = advance(firefly[0], firefly[1], firefly[2] * self.window.dt)
            firefly[1] += firefly[3] * self.window.dt

            if random.random() * 4 < self.window.dt:
                firefly[3] = random.random() * 4 * random.choice([-1, 1])
                firefly[2] = random.random() * 10 + 10

            wpos = (
                int(firefly[0][0] % self.display.get_width()),
                int(firefly[0][1] % self.display.get_height()),
            )

            self.renderer.blit({
                "source": self.firefly_img,
                "position": Position(wpos[0], wpos[1]),
            }, z_level=11)

            diameter = math.sin(firefly[2] * 0.2 + self.window.time) * 8 + 25
            glow_img = pyg.transform.scale(self.glow_img, (diameter, diameter))
            self.renderer.blit({
                "source": glow_img,
                "position": Position(
                    (wpos[0] - glow_img.get_width() // 2),
                    (wpos[1] - glow_img.get_height() // 2),
                ),
            }, z_level=107)

    def update(self) -> None:
        self.display.fill((21, 21, 21))
        self.ui_surf.fill((0, 0, 0, 0))

        self.text["large_font"].render_with(self.renderer, {
            "text": f"{round(self.window.fps)}",
            "loc": (self.display.get_rect().centerx, 0),
        })

        self.render_background()

        self.renderer.cycle({
            "default": self.display,
            "ui": self.ui_surf,
        })

        self.window.cycle({
            "surface": self.display,
            "ui_surf": self.ui_surf,
        })


def main() -> None:
    game = Game(
        width=1024,
        height=768,
        scale=3,
    )
    game.run()


if __name__ == '__main__':
    main()