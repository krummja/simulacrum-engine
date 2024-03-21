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
    imports: NotRequired[list[ModuleMeta]]
    providers: NotRequired[list[type[Provider]]]
    exports: NotRequired[list[type[Provider]]]


class ModuleDecorator:

    def __call__(self, metadata: ModuleMetadata):
        def wrapper(target: type):
            _target = target()
            for key in metadata:
                setattr(_target, key, metadata[key])
            return _target
        return wrapper


Module = ModuleDecorator()


TEST = "TEST"
class TestProvider:
    provide = TEST
    use_value: str = "test value"


class ModuleMeta(type):

    def __new__(cls, name, bases, namespace) -> ModuleMeta:
        clsobj = super().__new__(cls, name, bases, namespace)
        return clsobj


class OtherService:

    def __init__(self, test_value: TestProvider) -> None:
        self.test_value = test_value.use_value


OTHER_SERVICE = "OTHER_SERVICE"
class OtherServiceProvider:
    provide = OTHER_SERVICE
    use_class = OtherService


@Module({
    "imports": [],
    "providers": [
        OtherServiceProvider,
    ],
    "exports": [],
})
class OtherModule(metaclass=ModuleMeta):
    pass


@Module({
    "imports": [
        OtherModule,
    ],
    "providers": [
        TestProvider,
    ],
    "exports": [
        TestProvider,
    ],
})
class SomeModule(metaclass=ModuleMeta):
    pass


@Module({
    "imports": [
        OtherModule,
        SomeModule,
    ],
})
class AppModule(metaclass=ModuleMeta):
    pass


if __name__ == '__main__':
    app = AppModule()
    inspect(app, all=True)
