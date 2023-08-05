from __future__ import annotations

from functools import partial
from typing import Any, Callable, Dict, Iterable, Optional, Tuple

from stepizer.loader import Loader

ArgsType = Tuple[Any, ...]
KwargsType = Dict[str, Any]


class Step:
    def __init__(
        self,
        callable_: Callable,
        /,
        args: ArgsType = tuple(),
        kwargs: Optional[KwargsType] = None,
        name: Optional[str] = None,
        loader: Optional[Loader] = None,
        args_mapping: Tuple[str, ...] = ('',),
        kwargs_mapping: Optional[Dict[str, str]] = None,
        is_generator: bool = False,
        output_cache: str = 'ignore',
    ) -> None:
        self._callable = callable_
        self._args = args
        self._kwargs = kwargs or dict()
        self._name = name or self._callable.__name__
        self._loader = loader or Loader()
        self._args_mapping = args_mapping
        self._kwargs_mapping = kwargs_mapping or dict()
        self._is_generator = is_generator
        self._output_cache = output_cache
        self._next_step: Optional[Step] = None

        if self._is_generator:
            self._call = self._generator
        else:
            self._call = self._function

    @property
    def callable(self) -> Callable:
        return self._callable

    @property
    def args(self) -> ArgsType:
        return self._args

    @property
    def kwargs(self) -> KwargsType:
        return self._kwargs

    @property
    def name(self) -> str:
        return self._name

    @property
    def loader(self) -> Loader:
        return self._loader

    @property
    def args_mapping(self) -> Tuple[str, ...]:
        return self._args_mapping

    @property
    def kwargs_mapping(self) -> Dict[str, str]:
        return self._kwargs_mapping

    @property
    def is_generator(self) -> bool:
        return self._is_generator

    @property
    def output_cache(self) -> str:
        return self._output_cache

    @property
    def next_step(self) -> Optional[Step]:
        return self._next_step

    def iter_steps(self) -> Iterable[Step]:
        yield self
        if self._next_step:
            yield from self._next_step.iter_steps()

    @classmethod
    def wrap(cls, callable_: Callable) -> Step:
        if isinstance(callable_, cls):
            return callable_
        return cls(callable_)

    @classmethod
    def chain(cls, callable_: Callable, /, *callables: Callable) -> Step:
        step = cls.wrap(callable_)
        for c in callables:
            step.link(c)
        return step

    def link(self, callable_: Callable) -> Step:
        if self._next_step is None:
            self._next_step = Step.wrap(callable_)
        else:
            self._next_step.link(callable_)
        return self

    __or__ = link

    def __call__(self, *args, _cache: Optional[KwargsType] = None, **kwargs) -> Iterable[Any]:
        for outputs in self._loader(
            function=partial(self._generate_output, cache=_cache or dict()),
            outputs=self._call(*self._args, *args, **self._kwargs, **kwargs),
        ):
            yield from outputs

    def run(self, *args, **kwargs) -> Any:
        output = self(*args, **kwargs)
        if any(step._is_generator for step in self.iter_steps()):
            return list(output)
        return next(iter(output))

    def execute(self, *args, **kwargs) -> None:
        for _ in self(*args, **kwargs):
            pass

    def _get_arguments(self, output: Any, cache: KwargsType) -> Tuple[ArgsType, KwargsType]:
        def get_argument(name):
            return cache[name] if name else output

        args = tuple(get_argument(name) for name in self._args_mapping)
        kwargs = {argument: get_argument(name) for argument, name in self._kwargs_mapping.items()}
        return args, kwargs

    def _update_cache(self, output: Any, cache: KwargsType) -> KwargsType:
        if self._output_cache == 'ignore':
            return cache.copy()
        if self._output_cache == 'add':
            return {**cache, self._name: output}
        if self._output_cache == 'update':
            return {**cache, **output}
        raise ValueError(f"Output cache {self._output_cache} is not supported")

    def _generate_output(self, output: Any, cache: KwargsType) -> Iterable[Any]:
        if self._next_step is None:
            yield output
        else:
            cache = self._update_cache(output=output, cache=cache)
            args, kwargs = self._next_step._get_arguments(output=output, cache=cache)
            yield from self._next_step(*args, _cache=cache, **kwargs)

    def _function(self, *args, **kwargs) -> Iterable[Any]:
        yield self._callable(*args, **kwargs)

    def _generator(self, *args, **kwargs) -> Iterable[Any]:
        yield from self._callable(*args, **kwargs)
