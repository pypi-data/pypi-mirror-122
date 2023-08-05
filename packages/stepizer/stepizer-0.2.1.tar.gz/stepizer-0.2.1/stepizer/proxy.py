from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Iterable, Optional

if typing.TYPE_CHECKING:
    from stepizer.step import Step


class Proxy(metaclass=ABCMeta):
    def __init__(self, step: Step, cache: Optional[Dict[str, Any]] = None) -> None:
        self._step = step
        self._cache = cache or dict()

    def __call__(self, output: Any) -> Iterable[Any]:
        if self._step.next_step is None:
            yield output
        else:
            cache = {**self._cache, **self.update_cache(output)}
            _cache = {**cache, '': output}

            args = tuple(_cache[name] for name in self._step.next_step.map_args)
            kwargs = {key: _cache[name] for key, name in self._step.next_step.map_kwargs.items()}

            yield from self._step.next_step(*args, _cache=cache, **kwargs)

    @abstractmethod
    def update_cache(self, output: Any) -> Dict[str, Any]:
        raise NotImplementedError


class DefaultProxy(Proxy):
    def update_cache(self, output: Any) -> Dict[str, Any]:
        return dict()


class PersistentProxy(Proxy):
    def update_cache(self, output: Any) -> Dict[str, Any]:
        return {self._step.name: output}


class MultipleProxy(Proxy):
    def update_cache(self, output: Any) -> Dict[str, Any]:
        return output
