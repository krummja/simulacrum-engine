from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from simulacrum_engine.core.engine import Engine
    from simulacrum_engine.core.component import EngineComponent

import functools
import structlog
import colorama
from colors import color
from structlog.dev import Column, KeyValueColumnFormatter

from simulacrum_engine.core.component import EC
from simulacrum_engine.core.events import Events


def map_symbols(key: object | None = None) -> str:
    key = str(key)
    if key not in ["success", "warning", "error"] or key is None:
        return " "
    return color({
        'success': '✔',
        'warning': '⚠',
        'error': '✖'
    }[key], fg={
        'success': 'green',
        'warning': 'orange',
        'error': 'red',
    }[key])


cr = structlog.dev.ConsoleRenderer(
    columns=[
        Column(
            key='timestamp',
            formatter=KeyValueColumnFormatter(
                key_style=None,
                value_style='\x1b[2m',
                reset_style='\x1b[0m',
                value_repr=str,
                width=0,
                prefix='',
                postfix='',
            ),
        ),
        Column(
            key='level',
            formatter=structlog.dev.LogLevelColumnFormatter(
                level_styles=structlog.dev.ConsoleRenderer.get_default_level_styles(),
                reset_style=structlog.dev._ColorfulStyles.reset,
            ),
        ),
        Column(
            key="symbol",
            formatter=KeyValueColumnFormatter(
                key_style=None,
                value_style='\x1b[1m',
                reset_style='\x1b[0m',
                value_repr=map_symbols,
                width=0,
                prefix='[ ',
                postfix=' ]',
            ),
        ),
        Column(
            key='event',
            formatter=KeyValueColumnFormatter(
                key_style=None,
                value_style='\x1b[1m',
                reset_style='\x1b[0m',
                value_repr=str,
                width=30,
                prefix='',
                postfix='',
            ),
        ),
        Column(
            key='logger',
            formatter=KeyValueColumnFormatter(
                key_style=None,
                value_style='\x1b[1m\x1b[34m',
                reset_style='\x1b[0m',
                value_repr=str,
                width=0,
                prefix='[',
                postfix=']',
            ),
        ),
        Column(
            key='logger_name',
            formatter=KeyValueColumnFormatter(
                key_style=None,
                value_style='\x1b[1m\x1b[34m',
                reset_style='\x1b[0m',
                value_repr=str,
                width=0,
                prefix='[',
                postfix=']',
            ),
        ),
        Column(
            "",
            structlog.dev.KeyValueColumnFormatter(
                key_style=colorama.Fore.CYAN,
                value_style=colorama.Fore.GREEN,
                reset_style=colorama.Style.RESET_ALL,
                value_repr=str,
            ),
        ),
    ]
)

structlog.configure(processors=structlog.get_config()["processors"][:-1]+[cr])


class Logger:

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        self.emitter = self.engine.emitter
        self.log = structlog.get_logger()

        self.emitter.on(Events.LOG_INFO, self.info)

    def info(self, message: str, symbol: str | None = None, **extra: Any) -> None:
        self.log.info(message, symbol=symbol, **extra)




class BootParams(TypedDict):
    pass


P = TypeVar("P", bound=BootParams, covariant=True)

BootFunction: TypeAlias = Callable[[EC, P], bool]

M = TypeVar("M", bound=BootFunction)

class BootMethod(Protocol[M, P]):
    __call__: M


def log_boot(boot_method: BootMethod[M, P]) -> BootMethod:

    # functools.wraps(boot_method)
    def method_proxy(self: EngineComponent, params: BootParams | None = None) -> bool:
        boot_result = boot_method(self, params)
        return boot_result

        # self.engine.emitter.emit(
        #     Events.LOG_INFO,
        #     message=f"{self.id} booted.",
        #     symbol="success" if boot_result else "error",
        # )

    return method_proxy
