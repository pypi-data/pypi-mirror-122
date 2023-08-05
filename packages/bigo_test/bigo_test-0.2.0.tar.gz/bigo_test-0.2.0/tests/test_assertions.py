# -*- coding: utf-8 -*-
import unittest

from bigo_test.assertions import assertBigO
from bigo_test.complexity import Linear, Quadratic
from bigo_test.exceptions import WrongTimeComplexity


class TestBasicAssertions(unittest.TestCase):
    def test_simple_sorting_function_assertion(self):
        def max_function(number_list):
            max_ = 0
            for el in number_list:
                if el > max_:
                    max_ = el
            return max_

        def input_generator(numbers):
            return list(range(numbers))

        assertBigO(max_function, input_generator, Linear)

        with self.assertRaises(WrongTimeComplexity):
            assertBigO(max_function, input_generator, Quadratic)

    def test_quadratic_complexity(self):
        def bad_max_function(number_list):
            max_ = 0
            for el in number_list:
                if el > max_:
                    max_ = el

                # To bump the time complexity to n^2
                for el in number_list:
                    pass

            return max_

        def input_generator(numbers):
            return list(range(numbers))

        with self.assertRaisesRegex(WrongTimeComplexity, "Expected 'Linear' but fitted time complexity is 'Quadratic'"):
            assertBigO(
                bad_max_function,
                input_generator,
                Linear,
                timer_options={"minimum_n": 100, "maximum_n": 1000, "n_count": 10},
            )


if __name__ == "__main__":
    unittest.main()
