# -*- coding: utf-8 -*-
import unittest
from time import sleep
import numpy as np

from bigo_test.assertions.helpers import execution_timer


def test_func_factory(n):
    def func(a):
        # pylint: disable=unused-argument
        sleep(n)

    return func


class TestHelpers(unittest.TestCase):
    def test_execution_timer(self):
        func = test_func_factory(1)
        numbers, times = execution_timer(func, lambda x: x, options={"minimum_n": 1, "maximum_n": 1, "n_count": 2})

        np.testing.assert_array_equal(numbers, np.array([1, 1]))
        np.testing.assert_almost_equal(times, np.array([1, 1]), decimal=1)

    def test_execution_timer_defaults(self):
        func = test_func_factory(1)
        numbers, times = execution_timer(func)

        np.testing.assert_array_equal(numbers, np.array([1, 1]))
        np.testing.assert_almost_equal(times, np.array([1, 1]), decimal=1)

    def test_execution_timer_maximum_n_lesser_than_minimum_n(self):
        func = test_func_factory(1)
        numbers, times = execution_timer(func, options={"minimum_n": 2, "maximum_n": 1})

        np.testing.assert_array_equal(numbers, np.array([2, 2]))
        np.testing.assert_almost_equal(times, np.array([1, 1]), decimal=1)


if __name__ == "__main__":
    unittest.main()
