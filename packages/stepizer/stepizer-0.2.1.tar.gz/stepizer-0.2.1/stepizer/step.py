from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, Optional, Tuple, Type, Union

from stepizer.loader import Loader
from stepizer.proxy import Proxy
from stepizer.register import loaders, proxies


class Step:
    def __init__(
        self,
        _callable: Callable,
        /,
        args: Tuple[Any, ...] = tuple(),
        kwargs: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
        loader: Union[Loader, str] = 'function',
        loader_kwargs: Optional[Dict[str, Any]] = None,
        proxy_class: Union[Type[Proxy], str] = 'default',
        map_args: Tuple[str, ...] = ('',),
        map_kwargs: Optional[Dict[str, str]] = None,
    ) -> None:
        self._callable = _callable
        self._args = args
        self._kwargs = kwargs or dict()
        self._name = name or self._callable.__name__
        self._loader = loaders.init(loader, **(loader_kwargs or dict()))
        self._proxy_class = proxies.get(proxy_class)
        self._map_args = map_args
        self._map_kwargs = map_kwargs or dict()
        self._next_step: Optional[Step] = None

    @property
    def callable(self) -> Callable:
        return self._callable

    @property
    def name(self) -> str:
        return self._name

    @property
    def loader(self) -> Loader:
        return self._loader

    @property
    def proxy_class(self) -> Type[Proxy]:
        return self._proxy_class

    @property
    def map_args(self) -> Tuple[str, ...]:
        return self._map_args

    @property
    def map_kwargs(self) -> Dict[str, str]:
        return self._map_kwargs

    @property
    def next_step(self) -> Optional[Step]:
        return self._next_step

    def iter_steps(self) -> Iterable[Step]:
        yield self
        if self._next_step:
            yield from self._next_step.iter_steps()

    @classmethod
    def wrap(cls, _callable: Callable, /) -> Step:
        if isinstance(_callable, cls):
            return _callable
        return cls(_callable)

    @classmethod
    def chain(cls, _callable: Callable, /, *callables: Callable) -> Step:
        step = cls.wrap(_callable)
        for c in callables:
            step.link(c)
        return step

    def link(self, _callable: Callable, /) -> Step:
        if self._next_step is None:
            self._next_step = Step.wrap(_callable)
        else:
            self._next_step.link(_callable)
        return self

    __or__ = link

    def __call__(self, *args, _cache: Optional[Dict[str, Any]] = None, **kwargs) -> Iterable[Any]:
        proxy = self._proxy_class(step=self, cache=_cache)
        output = self._callable(*self._args, *args, **self._kwargs, **kwargs)
        for output in self._loader(function=proxy, output=output):
            yield from output

    def run(self, *args, **kwargs) -> Any:
        output = self(*args, **kwargs)
        if all(step._loader.exactly_one_output for step in self.iter_steps()):
            return next(iter(output))
        return list(output)

    def execute(self, *args, **kwargs) -> None:
        for _ in self(*args, **kwargs):
            pass
