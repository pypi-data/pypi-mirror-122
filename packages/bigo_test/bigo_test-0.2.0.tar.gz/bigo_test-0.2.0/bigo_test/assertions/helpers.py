# -*- coding: utf-8 -*-
from timeit import Timer
from typing import Callable, Optional, Tuple
import numpy as np
from numpy.typing import NDArray


default_timer_options = {"minimum_n": 1, "maximum_n": 1, "n_count": 2, "repeat_count": 1, "num_times": 1}


def execution_timer(
    test_function: Callable, input_generator: Callable = lambda x: x, options: Optional[dict[str, int]] = None,
) -> Tuple[NDArray[float], NDArray[float]]:
    if options is None:
        options = default_timer_options
    # Get values from the timer options
    minimum_n = options.get("minimum_n", default_timer_options.get("minimum_n"))
    maximum_n = options.get("maximum_n", default_timer_options.get("maximum_n"))
    n_count = options.get("n_count", default_timer_options.get("n_count"))
    repeat_count = options.get("repeat_count", default_timer_options.get("repeat_count"))
    num_times = options.get("num_times", default_timer_options.get("num_times"))

    if minimum_n > maximum_n:
        maximum_n = minimum_n

    # A wrapper which calls the function we need to time using timeit Timer
    class func_wrapper:
        def __init__(self, n):
            self.data = input_generator(n)

        def __call__(self):
            return test_function(self.data)

    ns = np.linspace(minimum_n, maximum_n, n_count).astype("int64")
    execution_time = np.empty(n_count)
    for i, n in enumerate(ns):
        timer = Timer(func_wrapper(n))
        measurements = timer.repeat(num_times, repeat_count)
        execution_time[i] = np.min(measurements)
    return ns, execution_time
