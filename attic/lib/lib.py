from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import functools
from devtools import debug
from rich import inspect


T = TypeVar("T")


class ClassProvider(Protocol, Generic[T]):
    provide: str
    use_class: type[T]


class ValueProvider(Protocol, Generic[T]):
    provide: str
    use_value: T


Provider = ClassProvider | ValueProvider


class GetOrCreateMetadataMap:

    def __init__(self) -> None:
        pass

    def __call__(self, obj: object, key: str) -> dict[Any, Any]:

        return {}


class ModuleMetadata(TypedDict):
    imports: NotRequired[list[Any]]
    providers: NotRequired[list[Provider]]
    exports: NotRequired[list[Any]]


class ModuleDecorator:

    def __call__(self, metadata: ModuleMetadata):
        def wrapper(target: type):
            _target = target()
            for key in metadata:
                setattr(target, key, metadata[key])
            return target
        return wrapper


Module = ModuleDecorator()


class TestProvider:
    provide = "TEST"
    use_value: str


@Module({
    "imports": [],
    "providers": [
        TestProvider(),
    ],
    "exports": [],
})
class SomeModule:

    def __init__(self, test_provider: TestProvider) -> None:
        self.test_provider = test_provider


if __name__ == '__main__':
    module = SomeModule()
    inspect(module, all=True)
