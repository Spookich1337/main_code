import numpy as np
from scipy.integrate import quad

def f(x):
    return np.cos(x ** 2)

def rectangle(a, b, n):
    h = (b - a) / n
    integral = 0
    for i in range(n):
        x_i = a + (i + 0.5) * h
        integral += f(x_i)
    return h * integral

def trapezoid(a, b, n):
    h = (b - a) / n
    x = a
    integral = 0
    for _ in range(n):
        integral += f(x) + f(x + h)
        x += h
    return integral * h / 2

def simpson(a, b, n):
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    integral = f(a) + f(b)
    for i in range(1, n):
        if i % 2 == 0:
            integral += 2 * f(a + i * h)
        else:
            integral += 4 * f(a + i * h)
    return (h / 3) * integral

def runge_estimate(method, a, b, n, epsilon):
    k = {
        rectangle: 1,
        trapezoid: 3,
        simpson: 15
    }[method]
    while True:
        integral_n = method(a, b, n)
        integral_2n = method(a, b, 2 * n)
        R = abs(integral_2n - integral_n) / k
        if R < epsilon:
            return integral_2n + R, 2 * n
        n *= 2


def test_integrations(a, b, digital_precision):
    epsilons = [10 ** (-x) for x in range(1, digital_precision + 1)]
    integral_exact, error = quad(f, a, b)
    methods = [
        (rectangle, "Rectangle"),
        (trapezoid, "Trapezoid"),
        (simpson, "Simpson")
    ]

    print(f"{'Method':<12} {'Epsilon':<10} {'Result':<12} {'N':<6} {'Difference':<10}")

    for epsilon in epsilons:
        round_to = abs(int(np.log10(epsilon)))
        for method, name in methods:
            result, n = runge_estimate(method, a, b, 2, epsilon)
            diff = round(abs(result - integral_exact), round_to)
            result = round(result, round_to)
            print(f"{name:<12} {epsilon:<10.1e} {result:<12} {n:<6} {diff:<10}")
    print(f"\nScipy result {round(integral_exact, digital_precision + 1)}")

def main(digital_precision):
    test_integrations(0, 1, 5)

main(6)

