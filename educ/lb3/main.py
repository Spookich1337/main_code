import math
import numpy as np
from scipy.optimize import bisect as scipy_bisect
import matplotlib.pyplot as plt
import random

def f(x):
    return 1 / (3 + 2 * math.cos(x)) - x**3

def Round(x, delta):
    if delta == 0.0:
        return x  # Без округления
    error = random.uniform(-delta / 2, delta / 2)
    return x + error

def error_f(x, delta):
    return Round(f(x), delta)

def Bisect_with_error(left, right, epsilon, delta):
    iter_count = 0
    while (right - left) / 2 > epsilon:
        middle = (left + right) / 2
        f_middle = error_f(middle, delta)
        f_left = error_f(left, delta)

        if f_middle == 0:
            return middle, iter_count

        if f_left * f_middle < 0:
            right = middle
        else:
            left = middle

        iter_count += 1

    return (left + right) / 2, iter_count

def explore_iterations_by_eps(left, right, eps_values, delta):
    iterations = []
    for eps in eps_values:
        _, iter_count = Bisect_with_error(left, right, eps, delta)
        iterations.append(iter_count)
    return iterations

def plot_iterations(left, right, eps_values):
    eps_values_reversed = sorted(eps_values, reverse=True)
    iterations = explore_iterations_by_eps(left, right, eps_values_reversed, 0)

    plt.figure(figsize=(10, 6))
    plt.plot(eps_values_reversed, iterations, marker='o', label=f'Iterations', color="red")
    plt.xscale('log')
    plt.yscale('linear')
    plt.xlabel('Eps (точность)')
    plt.ylabel('Число итераций')
    plt.title(f'Зависимость числа итераций от точности Eps')
    plt.legend()
    plt.grid(True)
    plt.show()

def test_bisect_with_error(left, right):
    eps_values = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
    delta_values = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
    print("Таблица: Влияние delta и eps на значение корня")
    print(f"{'delta':<10} {'eps':<10} {'Root':<15} {'Scipy':<15} {'Error':<10}")

    for delta in delta_values:
        for eps in eps_values:
            root, _ = Bisect_with_error(left, right, eps, delta)
            exact_root = scipy_bisect(f, left, right, xtol=delta)
            error = abs(root - exact_root)
            print(f"{delta:<10} {eps:<10} {root:<15.6f} {exact_root:<15.6f} {error:<10.6f}")


# left, right = map(float, input("Введите границы [left right]: ").split())
# test_bisect_with_error(left, right)
# eps_values = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
# plot_iterations(left, right, eps_values)
print(Bisect_with_error(0, 1, 10**-6, 0))