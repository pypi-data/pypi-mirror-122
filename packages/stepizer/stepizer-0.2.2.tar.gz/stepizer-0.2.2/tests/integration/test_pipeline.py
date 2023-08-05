from typing import Iterable, List

from stepizer.step import Step
from tests.integration import IntegrationCase


def add_text(string: str) -> str:
    return 'hello, ' + string + '!'


class TestBasicPipeline(IntegrationCase):
    def setUp(self) -> None:
        self.pipeline = Step.chain(
            add_text,
            str.upper,
        )

    def test_pipeline(self) -> None:
        actual = self.pipeline.run('world')

        self.assertEqual('HELLO, WORLD!', actual)


def read_paths(directory: str) -> Iterable[str]:
    for i in range(3):
        yield f'{directory}/image_{i}.jpg'


def read_image(path: str) -> List[int]:
    return [ord(char) for char in path]


def detect_objects(image: List[int]) -> Iterable[List[int]]:
    for i in range(5, 7):
        yield image[-i:]


def save(obj: List[int], path: str) -> str:
    return path + f'.{sum(obj)}.save'


class TestAdvancedPipeline(IntegrationCase):
    def setUp(self) -> None:
        self.pipeline = (
            Step(read_paths, loader='generator', proxy='single')
            | read_image
            | Step(detect_objects, loader='generator')
            | Step(save, map_args=('', 'read_paths'))
        )

    def test_pipeline(self) -> None:
        expected = [
            'dir/image_0.jpg.415.save',
            'dir/image_0.jpg.510.save',
            'dir/image_1.jpg.416.save',
            'dir/image_1.jpg.511.save',
            'dir/image_2.jpg.417.save',
            'dir/image_2.jpg.512.save',
        ]

        actual = self.pipeline.run('dir')

        self.assertListEqual(expected, actual)
