from typing import Any, Iterable

from stepizer.step import Step
from tests.benchmark import BenchmarkCase
from tests.benchmark.utils import timeit


def function(prefix: str, number: int = 5) -> Iterable[str]:
    for i in range(number):
        x = sum([a ** i for a in range(1000)])
        yield f"{prefix}.{x}-{i}"


def baseline_pipeline(*args, **kwargs) -> Any:
    out = []
    for x1 in function(*args, **kwargs):
        for x2 in function(x1):
            for x3 in function(x2):
                out.append(x3)
    return out


class TestDefaultPipeline(BenchmarkCase):
    def setUp(self) -> None:
        self.pipeline = Step.chain(
            Step(function, loader='generator'),
            Step(function, loader='generator'),
            Step(function, loader='generator'),
        )

    def test_pipeline(self) -> None:
        baseline_time = timeit(30, baseline_pipeline, 'start', 15)
        pipeline_time = timeit(30, self.pipeline.run, 'start', 15)

        self.assertAlmostEqual(baseline_time, pipeline_time, places=2)
