from unittest.mock import Mock

from stepizer.loader import Loader
from stepizer.proxy import DefaultProxy
from stepizer.step import Step
from tests.unit import UnitCase


class TestStepProperties(UnitCase):
    def setUp(self) -> None:
        self.callable = Mock(__name__='Mock')
        self.step = Step(self.callable)

    def test_callable(self) -> None:
        function = self.step.callable

        self.assertIs(function, self.callable)

    def test_name(self) -> None:
        name = self.step.name

        self.assertIsInstance(name, str)
        self.assertEqual(self.callable.__name__, name)

    def test_loader(self) -> None:
        loader = self.step.loader

        self.assertIsInstance(loader, Loader)

    def test_proxy(self) -> None:
        proxy = self.step.proxy

        self.assertIs(proxy, DefaultProxy)

    def test_map_args(self) -> None:
        map_args = self.step.map_args

        self.assertIsInstance(map_args, tuple)

    def test_map_kwargs(self) -> None:
        map_kwargs = self.step.map_kwargs

        self.assertIsInstance(map_kwargs, dict)

    def test_next_step(self) -> None:
        next_step = self.step.next_step

        self.assertIsNone(next_step)
