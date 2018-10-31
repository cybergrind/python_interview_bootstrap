"""
We expect only valid inputs here, so there are no validations here
"""
import math
import sys
from functools import lru_cache


@lru_cache(maxsize=None)
def fibonacci(n):
    """
    We're caching results here.
    That gives us single recursion call fin(n-1) and fib(n-2) we're getting from the cache
    """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def factorial(n):
    return math.factorial(n)


def ackermann(m, n):
    """
    In general it doesn't have a lot of sense to calculate function directly
    It woule be better to implement separate strategy to each m row
    according wiki section `Table of values`
    """
    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))
