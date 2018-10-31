import os

import pytest


@pytest.fixture
def ackermann_data():
    yield [
        [(0, 0), 1],
        [(0, 1), 2],
        [(1, 0), 2],
        [(1, 1), 3],
        [(2, 0), 3],
        [(2, 1), 5],
        [(3, 4), 125],
    ]


@pytest.fixture
def factorial_data():
    yield [[0, 1], [1, 1], [6, 720], [7, 5040]]


@pytest.fixture
def fibonacci_data():
    yield [
        [0, 0],
        [1, 1],
        [2, 1],
        [3, 2],
        [4, 3],
        [5, 5],
        [6, 8],
        [
            399,
            108_788_617_463_475_645_289_761_992_289_049_744_844_995_705_477_812_699_099_751_202_749_393_926_359_816_304_226,  # noqa
        ],
        [100, 354_224_848_179_261_915_075],
    ]


def pytest_configure(config):
    os.environ['LOG_DIR'] = '/tmp/'
