from service.functions import ackermann, factorial, fibonacci


def test_factorial(factorial_data):
    for x, y in factorial_data:
        assert factorial(x) == y


def test_ackermann(ackermann_data):
    for x, y in ackermann_data:
        assert ackermann(*x) == y


def test_fibonacci(fibonacci_data):
    for x, y in fibonacci_data:
        assert fibonacci(x) == y
