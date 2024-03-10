from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from pathlib import Path
import math
import random

import pygame as pyg
from pygame.locals import *

import simulacrum_engine as siml
from simulacrum_engine.renderer import Position


TEST_DIR = Path(__file__).parent.resolve()
CONFIG = Path(TEST_DIR, "config.json")


def advance(vec, angle, amt):
    vec[0] += math.cos(angle) * amt
    vec[1] += math.sin(angle) * amt
    return vec


def load_png(filename: str) -> tuple[pyg.Surface, pyg.Rect]:
    path = Path(TEST_DIR, filename)
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

    def load(self) -> None:
        self.window = siml.Window(
            dimensions=(960, 630),
            title="Test Title",
            opengl=True,
        )

        self.input = siml.Input(CONFIG)
        self.window.bind_input(self.input)

        self.renderer = siml.Renderer()
        self.renderer.set_groups(["ui", "default"])

        self.display = pyg.Surface((960, 630))
        self.ui_surf = pyg.Surface((960, 630), pyg.SRCALPHA)

        font = pyg.font.Font(None, 36)
        self.text = font.render("Hello World!", True, (255, 255, 255))
        self.textpos = self.text.get_rect()
        self.textpos.centerx = self.display.get_rect().centerx

        self.glow_img = pyg.Surface((255, 255))
        self.glow_img.fill((round(174 * 0.2), round(266 * 0.2), round(255 * 0.3)))

        glow_img, glow_rect = load_png("light.png")
        self.glow_img.blit(
            glow_img,
            (0, 0),
            special_flags=pyg.BLEND_RGBA_MULT,
        )

        self.fireflies = []
        for _ in range(20):
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

        self.renderer.blit({
            "source": self.text,
            "position": Position(self.textpos.x, self.textpos.y),
        }, z_level=1)

        self.render_background()

        self.renderer.cycle({
            "default": self.display,
            "ui": self.ui_surf,
        })

        self.window.cycle({
            "surface": self.display,
            "ui_urf": self.ui_surf,
        })


def main() -> None:
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
