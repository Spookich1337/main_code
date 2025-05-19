import random
import scipy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


def generate_diagonal_dominant(n, interval):
    matrix = [[random.uniform(-interval, interval + 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        row_sum = sum(abs(matrix[i][j]) for j in range(n) if i != j)
        matrix[i][i] = row_sum + random.uniform(1, interval)
    b = [random.uniform(-interval, interval) for _ in range(n)]
    return matrix, b


def prepare_jacobi_matrix(n, matrix, b, epsilon):
    jacobi_matrix = []
    for i in range(n):
        if abs(matrix[i][i]) < epsilon:
            raise ValueError(f"Матрица вырождена, нулевой элемент в строке {i}")
        row = []
        for j in range(n):
            if i != j: row.append(-matrix[i][j] / matrix[i][i])
            else: row.append(0.0)
        jacobi_matrix.append(row)
    initial_approach = [b[i] / matrix[i][i] for i in range(n)]
    return jacobi_matrix, initial_approach


def jacobi_solve(n, epsilon, matrix, b):
    jacobi_matrix, initial_approach = prepare_jacobi_matrix(n, matrix, b, epsilon)
    approaches = [initial_approach]
    prev_approach = initial_approach
    iteration = 1
    max_iter = 1000
    while iteration < max_iter:
        current_approach = []
        for i in range(n):
            sigma = 0.0
            for j in range(n):
                sigma += jacobi_matrix[i][j] * prev_approach[j]
            current_approach.append(initial_approach[i] + sigma)
        approaches.append(current_approach)
        iteration += 1
        if max(abs(current - previous) for current, previous in zip(current_approach, prev_approach)) < epsilon:
            return current_approach, approaches, iteration
        prev_approach = current_approach
    print(f"Достигнут лимит итераций {max_iter} точность не достигнута")


def convert_epsilon(digit_epsilon):
    return float(10 ** (-digit_epsilon))


print("Input size")
size = int(input())
print("Input interval")
inter = int(input())
print("Input epsilon")
eps_std = int(input())
eps = convert_epsilon(eps_std)
matrix, b = generate_diagonal_dominant(size, inter)

approach, approaches, iteration = jacobi_solve(size, eps, matrix, b)
# residual = compute_residual_norm(matrix, approach, b)
scipy_solution = scipy.linalg.solve(matrix, b)
print("Norm of diff:", np.linalg.norm(np.array(approach) - np.array(scipy_solution)))
# print(f"{'Approach:':<20}{'Scipy':<15}{'Diff':<15}")
max_display = 20
format_epsilon = f".{eps_std}f"
# for i in range(min(size, max_display)):
#     diff = abs(approach[i] - scipy_solution[i])
#     print("{:<15} {:<15} {:<15}".format(
#         f"{approach[i]:{format_epsilon}}",
#         f"{scipy_solution[i]:{format_epsilon}}",
#         f"{diff:.2e}"
#     ))
print(f"\nIterations: {iteration}")