# -*- coding: utf-8 -*-
"""
bigo_test module provides assersions and common time complexity class for asserting
functions have the expected time complexity

usage:
>>> from bigo_test import assertBigO
>>> from bigo_test.complexity import Linear, Quadratic
>>> def max_function(number_list):
...     max_ = 0
...     for el in number_list:
...         if el > max_:
...             max_ = el
...     return max_
>>> assertBigO(test_function, lambda x: x, Linear, timer_options={ "minimum_n": 100, "maximum_n": 10000, "n_count": 10})
WrongTimeComplexity: Expected 'Linear' but fitted time complexity is 'Quadratic'
>>> assertBigO(test_function, lambda x: x, Quadratic)
>>>
"""

__version__ = "0.2.0"
