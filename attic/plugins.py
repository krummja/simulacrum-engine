from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from enum import StrEnum
from devtools import debug

from simulacrum_engine._types import Bases
from simulacrum_engine._types import Namespace
from simulacrum_engine.events import Emitter


class Events(StrEnum):
    BOOT = "BOOT"
    READY = "READY"
    TEARDOWN = "TEARDOWN"


class PluginRegistry(type):

    REGISTRY = {}
    BOOTED = {}

    emitter: Emitter
    plugin_id: str

    def __new__(cls, name: str, bases: Bases, namespace: Namespace) -> PluginRegistry:
        clsobj = super().__new__(cls, name, bases, namespace)
        if name != "Plugin":
            clsobj.emitter = Emitter()
            clsobj.plugin_id = clsobj.__name__.upper()
            cls.REGISTRY[clsobj.plugin_id] = clsobj
        return clsobj

    @classmethod
    def plugins(cls) -> dict[str, type[Plugin]]:
        return cls.REGISTRY

    @classmethod
    def add_booted(cls, plugin: Plugin) -> None:
        cls.BOOTED[plugin.__class__.__name__] = plugin

    @classmethod
    def get_plugin(cls, key: str) -> Plugin:
        if key in cls.BOOTED:
            return cls.BOOTED[key]
        return cls.REGISTRY[key]


class Plugin(metaclass=PluginRegistry):

    def on_boot(self) -> None:
        raise NotImplementedError("Method must be implemented")

    def on_ready(self) -> None:
        raise NotImplementedError("Method must be implemented")

    def on_teardown(self) -> None:
        raise NotImplementedError("Method must be implemented")

    def boot(self, *args: Any, **kwargs: Any) -> None:
        self.on_boot()

    def ready(self, *args: Any, **kwargs: Any) -> None:
        self.on_ready()

    def teardown(self, *args: Any, **kwargs: Any) -> None:
        self.on_teardown()


class RootPlugin(Plugin):

    def on_boot(self) -> None:
        self.emitter.emit(Events.BOOT)

    def on_ready(self) -> None:
        self.emitter.emit(Events.READY)

    def on_teardown(self) -> None:
        self.emitter.emit(Events.TEARDOWN)


class PluginManager:

    def __init__(self, root_plugin: Plugin = RootPlugin()) -> None:
        self.boot_status: dict[str, bool] = {}
        self.root_plugin = root_plugin
        PluginRegistry.add_booted(self.root_plugin)

        for key, plugin in PluginRegistry.plugins().items():
            if key == self.root_plugin.plugin_id:
                continue
            self.boot_status[key] = False
            self._boot_plugin(plugin)

    @property
    def all_ready(self) -> bool:
        return all([value is True for value in self.boot_status.values()])

    def boot(self) -> None:
        self.root_plugin.boot()

    def _boot_plugin(self, plugin: type[Plugin]) -> Plugin:
        _plugin = plugin()
        PluginRegistry.add_booted(_plugin)
        self.root_plugin.emitter.on(Events.BOOT, _plugin.boot)
        self.root_plugin.emitter.on(Events.READY, _plugin.ready)
        self.root_plugin.emitter.on(Events.TEARDOWN, _plugin.teardown)
        self.boot_status[_plugin.plugin_id] = True
        return _plugin
