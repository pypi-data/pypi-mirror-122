def factorial(n):
    result = 1
    for x in range(2, n + 1):
        result *= x
    return result


def fibonacci(n):
    if n <= 2:
        return 1
    a, b = 1, 1
    for i in range(3, n + 1):
        a, b = b, a + b
    return b
