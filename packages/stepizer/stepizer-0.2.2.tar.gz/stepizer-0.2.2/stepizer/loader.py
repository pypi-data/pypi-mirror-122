from abc import ABCMeta, abstractmethod
from functools import partial
from multiprocessing import Pool
from typing import Any, Callable, Iterable, List, Optional


class Loader(metaclass=ABCMeta):
    @property
    @abstractmethod
    def exactly_one_output(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def __call__(self, function: Callable, output: Any) -> Iterable[Any]:
        raise NotImplementedError()


class FunctionLoader(Loader):
    @property
    def exactly_one_output(self) -> bool:
        return True

    def __call__(self, function: Callable, output: Any) -> Iterable[Any]:
        yield function(output)


class GeneratorLoader(Loader):
    @property
    def exactly_one_output(self) -> bool:
        return False

    def __call__(self, function: Callable, output: Iterable[Any]) -> Iterable[Any]:
        yield from map(function, output)


class BatchLoader(GeneratorLoader):
    def __init__(self, batch_size: int, collate: Optional[Callable] = None) -> None:
        self._batch_size = batch_size
        self._collate = collate

    def collate(self, outputs: List[Any]) -> Any:
        if self._collate is None:
            return outputs
        return self._collate(outputs)

    def __call__(self, function: Callable, output: Iterable[Any]) -> Iterable[Any]:
        batch = []
        for raw_output in output:
            batch.append(raw_output)
            if len(batch) == self._batch_size:
                output = self.collate(batch)
                yield function(output)
                batch = []

        if batch:
            output = self.collate(batch)
            yield function(output)


class MultiprocessingLoader(GeneratorLoader):
    @staticmethod
    def function(function: Callable, output: Any) -> List[Any]:
        return list(function(output))

    def __call__(self, function: Callable, output: Iterable[Any]) -> Iterable[Any]:
        with Pool() as pool:
            yield from pool.imap(partial(self.function, function), output)
