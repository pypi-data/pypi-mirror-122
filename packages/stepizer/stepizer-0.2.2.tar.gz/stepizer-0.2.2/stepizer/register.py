from typing import Dict, Generic, Iterator, Type, TypeVar, Union

from stepizer.loader import (
    BatchLoader, FunctionLoader, GeneratorLoader, Loader, MultiprocessingLoader)
from stepizer.proxy import DefaultProxy, MultiOutputProxy, Proxy, SingleOutputProxy

T = TypeVar('T')


class Register(Generic[T]):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self._items: Dict[str, Type[T]] = dict(**kwargs)

    def __getitem__(self, key: str) -> Type[T]:
        return self._items[key]

    def __setitem__(self, key: str, value: Type[T]) -> None:
        if key in self._items:
            raise KeyError(f"Cannot override {key} item")
        self._items[key] = value

    def __iter__(self) -> Iterator[str]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def init(self, _obj: Union[str, T], /, **kwargs) -> T:
        if isinstance(_obj, str):
            return self[_obj](**kwargs)  # type: ignore
        return _obj

    def get(self, _obj: Union[str, Type[T]], /) -> Type[T]:
        if isinstance(_obj, str):
            return self[_obj]
        return _obj


loaders: Register[Loader] = Register(
    batch=BatchLoader,
    function=FunctionLoader,
    generator=GeneratorLoader,
    multiprocessing=MultiprocessingLoader,
)

proxies: Register[Proxy] = Register(
    default=DefaultProxy,
    multi=MultiOutputProxy,
    single=SingleOutputProxy,
)
