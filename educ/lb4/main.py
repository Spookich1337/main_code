import math
import numpy as np
import random
import matplotlib.pyplot as plt

# Функция f(x)
def f(x):
    return 1 / (3 + 2 * math.cos(x)) - x**3

# Функция для добавления случайной ошибки
def add_error(x, delta):
    if delta == 0.0:
        return x
    error = random.uniform(-delta / 2, delta / 2)
    return x + error

def method_bisection(a, b, epsilon, delta):
    iter_count = 0
    while (b - a) / 2 > epsilon:
        iter_count += 1
        middle = (a + b) / 2
        f_middle = add_error(middle, delta)
        f_left = add_error(a, delta)

        if f_middle == 0:
            return middle, iter_count

        if f_left * f_middle < 0:
            b = middle
        else:
            a = middle
    return (a + b) / 2, iter_count

# Метод хорд с добавлением ошибки
def method_chord(a, b, epsilon, delta):
    if f(a) * f(b) >= 0:
        return -1, -1
    iteration = 0
    while True:
        iteration += 1

        a_value = add_error(f(a), delta)
        b_value = add_error(f(b), delta)

        # Вычисляем новое приближение
        c2 = a - (a_value * (b - a)) / (b_value - a_value)
        # Проверяем условие выхода
        if abs(f(c2)) < epsilon:
            return c2, iteration
        # Обновляем интервал
        if f(a) * f(c2) < 0:
            b = c2
        else:
            a = c2

def explore_iterations_bisection(left, right, eps_values):
    iterations = []
    for eps in eps_values:
        _, iter_count = method_bisection(left, right, eps, 0)
        iterations.append(iter_count)
    return iterations

def explore_iterations_chord(left, right, eps_values):
    iterations = []
    for eps in eps_values:
        _, iters = method_chord(left, right, eps, 0)
        iterations.append(iters)
    return iterations

def explore_error(left, right, eps_values):
    data = []
    for delta in eps_values:
        for eps in eps_values:
            if eps >= delta:
                root, iterations = method_chord(left, right, eps, delta)
                rounded_root = round(root, int(-np.log10(eps)))
                data.append([delta, eps, rounded_root, iterations])

    print("{:<10} {:<10} {:<15} {:<15}".format(
        "delta", "epsilon", "Значение корня", "Кол-во итераций"
    ))

    for row in data:
        delta, eps, root, iterations = row
        # Форматируем вывод с добавлением незначащих нулей
        print("{:<10} {:<10} {:<15} {:<15}".format(
            f"{delta:.6f}".rstrip('0').rstrip('.') if '.' in f"{delta:.6f}" else f"{delta:.6f}",
            f"{eps:.6f}".rstrip('0').rstrip('.') if '.' in f"{eps:.6f}" else f"{eps:.6f}",
            f"{root:.6f}".rstrip('0').rstrip('.') if '.' in f"{root:.6f}" else f"{root:.6f}",
            iterations
        ))

def plot_iterations(left, right, x0, eps_values):
    eps_values_reversed = sorted(eps_values, reverse=True)

    iterations_bisection = explore_iterations_bisection(left, right, eps_values_reversed)
    
    iterations_chord = explore_iterations_chord(left, right, eps_values_reversed)

    plt.figure(figsize=(10, 6))
    # График для метода Бисекции
    plt.plot(eps_values_reversed, iterations_bisection, marker="o", color="green", label="Метод Бисекции")
    # График для метода Хорд
    plt.plot(eps_values_reversed, iterations_chord, marker='o', color='blue', label='Метод Хорд')
   
   # Настройки графика
    plt.xscale('log')
    plt.yscale('linear')
    plt.xlabel('Eps (точность)')
    plt.ylabel('Число итераций')
    plt.title('Зависимость числа итераций от точности Eps')
    plt.yticks(range(0, 21, 1))
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

epsilons = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
plot_iterations(0, 1, 1, epsilons)
explore_error(0, 1, epsilons)