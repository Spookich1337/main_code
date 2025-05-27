import numpy as np
import matplotlib.pyplot as plt
import random

def divided_difference(x, y):
    """Вычисление разделенных разностей для полинома Ньютона"""

    coefficients = y.copy()
    for j in range(1, len(x)):
        for i in range(len(x) - 1, j - 1, -1):
            coefficients[i] = (coefficients[i] - coefficients[i - 1]) / (x[i] - x[i - j])
    return coefficients

def newton_interpolation(coefficients, x_nodes, x_target):
    """Интерполяция полиномом Ньютона в точке x_target"""

    result = coefficients[0]
    term = 1
    for i in range(1, len(coefficients)):
        term *= (x_target - x_nodes[i - 1])
        result += coefficients[i] * term
    return result

def chebyshev_nodes(a, b, n_nodes):
    j = np.arange(1, n_nodes + 1)
    nodes = np.cos((2 * j - 1) * np.pi / (2 * n_nodes))
    return 0.5 * (a + b) + 0.5 * (b - a) * nodes

def experiment(f, a, b):
    """Проводит эксперимент по интерполяции функции f на отрезке [a, b]"""
    x_plot = np.linspace(a, b, 1000)
    n_nodes = random.randint(5, 10)

    # Узлы и значения функции
    uniform_x = np.linspace(a, b, n_nodes)
    cheb_x = chebyshev_nodes(a, b, n_nodes)
    uniform_y = f(uniform_x)
    cheb_y = f(cheb_x)

    # Коэффициенты Ньютона
    uniform_coeffs = divided_difference(uniform_x, uniform_y)
    cheb_coeffs = divided_difference(cheb_x, cheb_y)

    # Интерполяции
    uniform_interp = [newton_interpolation(uniform_coeffs, uniform_x, x) for x in x_plot]
    cheb_interp = [newton_interpolation(cheb_coeffs, cheb_x, x) for x in x_plot]

    # Проверка в случайной точке
    x_target = random.uniform(a, b)
    exact_target = f(x_target)
    uniform_target = newton_interpolation(uniform_coeffs, uniform_x, x_target)
    cheb_target = newton_interpolation(cheb_coeffs, cheb_x, x_target)

    # График
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.plot(x_plot, f(x_plot), 'k-', label='Исходная функция', linewidth=2)
    plt.plot(x_plot, uniform_interp, 'b--', label=f'Равномерные узлы (n={n_nodes})')
    plt.plot(uniform_x, uniform_y, 'bo', markersize=8)
    plt.plot(x_plot, cheb_interp, 'r-.', label='Узлы Чебышёва')
    plt.plot(cheb_x, cheb_y, 'ro', markersize=8)
    plt.axvline(x=x_target, color='gray', linestyle='--', alpha=0.7)
    plt.legend()
    plt.title('Сравнение интерполяции Ньютона')
    plt.grid(True, alpha=0.3)

    plt.subplot(2, 1, 2)
    plt.plot(x_plot, np.abs(f(x_plot) - uniform_interp), 'b-', label='Ошибка (равномерные)')
    plt.plot(x_plot, np.abs(f(x_plot) - cheb_interp), 'r-', label='Ошибка (Чебышёв)')
    plt.axvline(x=x_target, color='gray', linestyle='--', alpha=0.7)
    plt.legend()
    plt.title('Погрешности интерполяции')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # Вывод результатов
    print(f"\nРезультаты для {n_nodes} узлов:")
    print(f"Точка интерполяции: x = {x_target:.4f}")
    print(f"Точное значение: f(x) = {exact_target:.6f}")
    print(f"Равномерные узлы: интерполяция = {uniform_target:.6f}, ошибка = {abs(exact_target - uniform_target):.2e}")
    print(f"Узлы Чебышёва: интерполяция = {cheb_target:.6f}, ошибка = {abs(exact_target - cheb_target):.2e}")

    print("\nРавномерные узлы:", np.round(uniform_x, 4))
    print("Узлы Чебышёва:", np.round(cheb_x, 4))

if __name__ == "__main__":
    func1 = lambda x: 1 / (3 + 2 * np.cos(x)) - x**3
    experiment(func1, 0, 1)