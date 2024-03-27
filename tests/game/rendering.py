from __future__ import annotations
from typing import *

import pygame as pyg
from simulacrum_engine import *
from simulacrum_engine.ecs.system import System

from tests import components


class RenderSystem(System):

    def initialize(self) -> None:
        self.renderer = self.engine[RenderManager].renderer
        self.ecs = self.loop.ecs
        self.animation_manager = self.engine[AnimationManager]

        self.query("renderables", all_of=[
            components.Renderable,
            components.Position,
        ])

    def update(self) -> None:
        renderables = self._queries["renderables"].result

        for entity in renderables:
            renderable = entity[components.Renderable]
            position = entity[components.Position]

            if renderable.surface is None:
                return

            if self.ecs.components.has(entity, components.Animatable):
                frame = entity[components.Animatable].next_frame
            elif self.ecs.components.has(entity, components.Sprite):
                frame = entity[components.Sprite].texture
            else:
                return

            if self.ecs.components.has(entity, components.Velocity):
                x = entity[components.Velocity].x
                y = entity[components.Velocity].y
                if x < 0 and not renderable.flipped_h:
                    entity.fire_event("set_flipped", data={
                        "flipped_h": True,
                    })
                if x > 0 and renderable.flipped_h:
                    entity.fire_event("set_flipped", data={
                        "flipped_h": False,
                    })

            renderable.update(frame)

            self.renderer.blit(
                params={
                    "source": renderable.surface,
                    "position": (position.x, position.y),
                },
                z_level=107 if renderable.alpha else 1,
            )
