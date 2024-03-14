from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from moderngl import Buffer
    from moderngl import Framebuffer
    from simulacrum_engine.shaderlib import MGL

import moderngl as mgl
import pygame as pyg


Uniform = mgl.Uniform | mgl.Texture | pyg.Surface


class RenderObject:

    def __init__(
        self,
        mgl: MGL,
        fragment: str,
        vertex: str | None = None,
        use_default: bool = False,
        vao_args: list[str] = ['2f 2f', 'vert', 'texcoord'],
        buffer: Buffer | None = None,
    ) -> None:
        self.use_default = use_default

        self.mgl = mgl
        self.frag_raw = fragment
        self.vert_raw = vertex
        self.vao_args = vao_args

        if not vertex:
            vertex = self.mgl.default_vert

        self.program = self.mgl.ctx.program(
            vertex_shader=vertex,
            fragment_shader=fragment,
        )

        if not buffer:
            buffer = self.mgl.quad_buffer

        self.vao = self.mgl.ctx.vertex_array(
            self.program,
            [(buffer, *vao_args)],
        )

        self.temp_textures = []
        self.debug = False

    def update(self, uniforms: dict[str, Uniform] | None = None) -> None:
        if uniforms is None:
            uniforms = {}

        texture_id = 0
        uniform_list = list(self.program)

        for uniform in uniforms:
            if uniform in uniform_list:
                if isinstance(uniforms[uniform], mgl.Texture):
                    cast(mgl.Texture, uniforms[uniform]).use(texture_id)
                    cast(mgl.Uniform, self.program[uniform]).value = texture_id
                    texture_id += 1
                else:
                    cast(mgl.Uniform, self.program[uniform]).value = uniforms[uniform]

    def render(
        self,
        dest: Framebuffer | None = None,
        uniforms: dict | None = None,
    ) -> None:
        if uniforms is None:
            uniforms = {}

        if dest is None:
            dest = self.mgl.ctx.screen

        dest.use()

        uniforms = self.parse_uniforms(uniforms)
        self.update(uniforms)
        self.vao.render(mode=mgl.TRIANGLE_STRIP)

        for texture in self.temp_textures:
            texture.release()
        self.temp_textures = []

    def parse_uniforms(self, uniforms: dict[str, Uniform]) -> dict[str, Uniform]:
        for name, value in uniforms.items():
            if isinstance(value, pyg.Surface):
                texture = self.mgl.pg_to_tex(value)
                uniforms[name] = texture
                self.temp_textures.append(texture)
        return uniforms
