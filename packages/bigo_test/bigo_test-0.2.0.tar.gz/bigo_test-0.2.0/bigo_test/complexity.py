# -*- coding: utf-8 -*-
from big_o import complexities


class BaseComplexity:
    pass


class Constant(complexities.Constant, BaseComplexity):
    pass


class Linear(complexities.Linear, BaseComplexity):
    pass


class Quadratic(complexities.Quadratic, BaseComplexity):
    pass


class Cubic(complexities.Cubic, BaseComplexity):
    pass


class Logarithmic(complexities.Logarithmic, BaseComplexity):
    pass


class Linearithmic(complexities.Linearithmic, BaseComplexity):
    pass


class Polynomial(complexities.Polynomial, BaseComplexity):
    pass


class Exponential(complexities.Exponential, BaseComplexity):
    pass
