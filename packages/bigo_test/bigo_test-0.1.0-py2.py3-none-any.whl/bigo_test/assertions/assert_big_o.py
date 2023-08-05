# -*- coding: utf-8 -*-
from typing import Callable, Optional
from big_o import complexities
from big_o.big_o import infer_big_o_class

from bigo_test.complexity import Constant, Cubic, Exponential, Linear, Linearithmic, Logarithmic, Polynomial, Quadratic
from bigo_test.exceptions import WrongTimeComplexity
from .base_assert import BaseAssertion
from .helpers import execution_timer


COMPLEXITIES_MAP = {
    complexities.Constant: Constant,
    complexities.Linear: Linear,
    complexities.Quadratic: Quadratic,
    complexities.Cubic: Cubic,
    complexities.Logarithmic: Logarithmic,
    complexities.Linearithmic: Linearithmic,
    complexities.Polynomial: Polynomial,
    complexities.Exponential: Exponential,
}


def assertBigO(
    test_function: Callable,
    input_generator: Callable,
    assertion_class: BaseAssertion,
    timer_options: Optional[dict[str, int]] = None,
):
    if timer_options is None:
        timer_options = {}
    timer_options = {
        "minimum_n": timer_options.get("minimum_n", 1000),
        "maximum_n": timer_options.get("maximum_n", 100000),
        "n_count": timer_options.get("n_count", 100),
        "repeat_count": timer_options.get("repeat_count", 1),
        "num_times": timer_options.get("num_times", 1),
    }
    numbers, times = execution_timer(test_function, input_generator=input_generator, options=timer_options)
    best, _ = infer_big_o_class(numbers, times)

    if type(best) not in COMPLEXITIES_MAP:
        raise NotImplementedError

    if COMPLEXITIES_MAP[type(best)] is not assertion_class:
        raise WrongTimeComplexity(
            f"Expected '{assertion_class.__name__}' but fitted time complexity is '{COMPLEXITIES_MAP[type(best)].__name__}'"
        )
