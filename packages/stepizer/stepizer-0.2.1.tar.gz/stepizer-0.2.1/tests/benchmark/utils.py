from time import time
from typing import Callable


def timeit(n: int, func: Callable, *args, **kwargs) -> float:
    times = list()
    for _ in range(n):
        start = time()
        func(*args, **kwargs)
        times.append(time() - start)
    return sum(times) / n
