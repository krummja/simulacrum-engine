from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import pygame as pyg


T = TypeVar("T", contravariant=True)


class RenderFunction(Protocol, Generic[T]):
    def __call__(self, surface: pyg.Surface, params: T, z_level: int) -> None:
        ...


class Renderable(NamedTuple, Generic[T]):
    render_function: RenderFunction[T]
    render_params: T
    z_level: int

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Renderable):
            return self.z_level < other.z_level
        return False


class BlitParams(TypedDict):
    source: pyg.Surface
    position: tuple[float, float]


class BlitFunction(RenderFunction[BlitParams]):

    def __call__(
        self,
        destination: pyg.Surface,
        params: BlitParams,
        z_level: int
    ) -> None:
        self.params = params
        self.z_level = z_level
        source = self.params["source"]
        position = self.params["position"]

        if z_level != 107:
            destination.blit(source, position)
        else:
            destination.blit(source, position, special_flags=pyg.BLEND_RGBA_ADD)


class Renderer:

    def __init__(self, groups: list[str] | None = None) -> None:
        self.groups = groups if groups else ["default"]
        self.render_queue: dict[str, list[Renderable]] = {}
        self.i = 0
        self.render_count = 0
        self.reset()

    def set_groups(self, groups: list[str]) -> None:
        self.groups = groups
        self.reset()

    def blit(
        self,
        params: BlitParams,
        z_level: int = 0,
        group: str = "default"
    ) -> None:
        """
        Calls `queue_render` with a default `RenderFunction` specified. Takes
        `BlitParams` and queues the function with its parameters in a prebuilt
        `Renderable`.
        """
        renderable = Renderable[BlitParams](
            render_function=BlitFunction(),
            render_params=params,
            z_level=z_level
        )
        self.queue_render(renderable, group)

    def queue_render(
        self,
        renderable: Renderable[T],
        group: str = "default",
    ) -> None:
        self.render_queue[group].append(renderable)
        self.i += 1

    def reset(self) -> None:
        for group in self.groups:
            self.render_queue[group] = []

    def cycle(self, dest_surfaces: dict[str, pyg.Surface]) -> dict[str, pyg.Surface]:
        """
        Process the render queue by iterating over the `Surface` objects in the
        `dest_surfaces` mapping.
        """
        self.render_count = 0

        for group in dest_surfaces:
            if group in self.render_queue:
                sorted(self.render_queue[group], key=lambda r: r.z_level)
                self.render_count += len(self.render_queue[group])

                for renderable in self.render_queue[group]:
                    function = renderable.render_function
                    params = renderable.render_params
                    function(dest_surfaces[group], params, renderable.z_level)

        self.reset()
        return dest_surfaces
