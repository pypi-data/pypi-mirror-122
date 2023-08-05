import unittest
from typing import Iterable, List

from stepizer.step import Step


def add_text(string: str) -> str:
    return 'hello, ' + string + '!'


class TestBasicPipeline(unittest.TestCase):
    def setUp(self) -> None:
        self.pipeline = Step.chain(
            add_text,
            str.upper,
        )

    def test_pipeline(self) -> None:
        actual = self.pipeline.run('world')
        print(actual)

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


class TestAdvancedPipeline(unittest.TestCase):
    def setUp(self) -> None:
        self.pipeline = (
            Step(read_paths, is_generator=True, output_cache='add')
            | read_image
            | Step(detect_objects, is_generator=True)
            | Step(save, args_mapping=('', 'read_paths'))
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
