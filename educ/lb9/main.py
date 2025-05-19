import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.interpolate import BarycentricInterpolator

def divided_difference(x, y):
    coefficients = y.copy()
    for j in range(1, len(x)):
        for i in range(len(x) - 1, j - 1, - 1):
            coefficients[i] = (coefficients[i] - coefficients[i - 1]) / (x[i] - x[i - j])
    return coefficients

def newton(coefficients, x_nodes, x_target):
    result = coefficients[0]
    term = 1
    for i in range(1, len(coefficients)):
        term *= (x_target - x_nodes[i - 1])
        result += coefficients[i] * term
    return result

def aitken(x, y, x_target):
    n = len(x)
    P = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        P[i][0] = y[i]

    for j in range(1, n):
        for i in range(n - j):
            xi, xj = x[i], x[i + j]
            Pi0 = P[i][j - 1]
            Pi1 = P[i + 1][j - 1]
            P[i][j] = ((x_target - xj) * Pi0 - (x_target - xi) * Pi1) / (xi - xj)

    return P[0][n - 1]

n_nodes = np.random.randint(5, 9)
x_nodes = sorted([random.uniform(-10, 10) for _ in range(n_nodes)])
y_values = sorted([random.uniform(-100, 100) for _ in range(n_nodes)])
x_target = random.uniform(min(x_nodes), max(x_nodes))

coefficients = divided_difference(x_nodes, y_values)

result = [
    newton(coefficients, x_nodes, x_target),
    aitken(x_nodes, y_values, x_target),
    BarycentricInterpolator(x_nodes, y_values)(x_target)
]

print(f"Сгенерировано {n_nodes} случайных узлов:"
      f"\nX: {x_nodes}"
      f"\nY: {y_values}"
      f"\nТочка интерполяции x = {x_target}")
print("\nРезультаты интерполяции:"
      f"\nМетод Ньютона: {result[0]}"
      f"\nМетод Эйткена: {result[1]}"
      f"\n{'Scipy':<13}: {result[2]}")

plt.figure(figsize=(12, 7))
plt.scatter(x_nodes, y_values, c='green', s=100, label='Узлы интерполяции', zorder=5)

plot_x = np.linspace(min(x_nodes), max(x_nodes), 200)
newton_y = [newton(coefficients, x_nodes, x) for x in plot_x]
aitken_y = [aitken(x_nodes, y_values, x) for x in plot_x]
scipy_y = BarycentricInterpolator(x_nodes, y_values)(plot_x)

plt.plot(plot_x, newton_y, 'b--', label='Полином Ньютона', linewidth=2)
plt.plot(plot_x, scipy_y, 'm-', label='Исходная функция', linewidth=1, alpha=0.7)

plt.title('Сравнение методов интерполяции на случайных данных', pad=20)
plt.xlabel('x', fontsize=12)
plt.ylabel('y', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("test.png")
plt.close()