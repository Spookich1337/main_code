import random
import scipy
import numpy as np

def validate_input(n, interval):
    if n < 3: raise ValueError("Matrix size must be above 3")
    if interval < 0 or interval > 1000000: raise ValueError("Interval must be above 0 or below 1000000")

def generate_extended_matrix(n, interval):
    matrix = [[random.uniform(0, interval) for _ in range(n)] for _ in range(n)]
    vectorB = [random.uniform(0, interval) for _ in range(n)]
    return [matrix[i] + [vectorB[i]] for i in range(n)]

def generate_hilbert_matrix(n, interval):
    matrix = [[1 / (i + j - 1) for j in range(1, n + 1)] for i in range(1, n + 1)]
    b = [random.uniform(0, interval) for _ in range(n)]
    return [matrix[i] + [b[i]] for i in range(n)]

def generate_diagonal_dominant(n, interval):
    matrix = [[random.uniform(0, interval) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        row_sum = sum([matrix[i][j] for j in range(n) if i != j])
        matrix[i][i] += row_sum
    b = [random.uniform(0, interval) for _ in range(n)]
    return [matrix[i] + [b[i]] for i in range(n)]

def straight_elimination(n, matrix):
    row_count = n
    column_count = n + 1
    for pivot_column in range(n):
        max_row = pivot_column
        for row in range(pivot_column + 1, row_count):
            if abs(matrix[row][pivot_column]) > abs(matrix[max_row][pivot_column]):
                max_row = row

        if abs(matrix[max_row][pivot_column]) == 0:
            raise ValueError("Система вырождена - ведущий элемент нулевой")
        matrix[pivot_column], matrix[max_row] = matrix[max_row], matrix[pivot_column]

        pivot = matrix[pivot_column][pivot_column]
        for i in range(pivot_column, column_count):
            matrix[pivot_column][i] /= pivot

        for row in range(pivot_column + 1, row_count):
            factor = matrix[row][pivot_column]
            for col in range(pivot_column, column_count):
                matrix[row][col] -= factor * matrix[pivot_column][col]

def inverse_step(n, matrix):
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        if abs(matrix[i][i]) == 0: continue
        x[i] = matrix[i][n]
        for c in range(i + 1, n):
            x[i] -= matrix[i][c] * x[c]
    return x

def gauss(matrix, n):
    A = [row[:-1] for row in matrix]
    b = [row[-1] for row in matrix]
    straight_elimination(n, matrix)
    my_solution = inverse_step(n, matrix)
    solution_scipy = scipy.linalg.solve(A, b)
    
    # Вычисление норм решений
    my_solution_norm = np.linalg.norm(my_solution, ord=2)
    scipy_solution_norm = np.linalg.norm(solution_scipy, ord=2)
    solution_diff_norm = np.linalg.norm(np.array(my_solution) - np.array(solution_scipy), ord=2)
    
    return {
        "custom_solution": my_solution,
        "scipy_solution": solution_scipy,
        "my_solution_norm": my_solution_norm,
        "scipy_solution_norm": scipy_solution_norm,
        "diff_solution_norm": solution_diff_norm,
        "residual_norm": compute_residual_norm(A, my_solution, b),
        "condition_number_custom": compute_conditional_digit(A, my_solution, b),
        "condition_number_scipy": np.linalg.cond(A)
    }

def compute_residual_norm(A, x, b):
    n = len(A)
    residual = [0.0] * n
    for i in range(n):
        Ax = sum(A[i][j] * x[j] for j in range(n))
        residual[i] = Ax - b[i]

    residual_norm = sum(r ** 2 for r in residual) ** 0.5
    b_norm = sum(b_i ** 2 for b_i in b) ** 0.5
    return residual_norm / b_norm

def compute_conditional_digit(A, x, b):
    A_inv = np.linalg.inv(A)
    norm_A = np.linalg.norm(A, ord=2)
    norm_A_inv = np.linalg.norm(A_inv, ord=2)
    return norm_A * norm_A_inv

def exploration(n, interval):
    names = ["Random", "Hilbert"]
    generators = [
        generate_extended_matrix,
        generate_hilbert_matrix
    ]

    results = []
    for name, generator in zip(names, generators):
        matrix = generator(n, interval)
        gauss_result = gauss(matrix, n)
        results.append({
            "matrix_type": name,
            "my_solution_norm": gauss_result["my_solution_norm"],
            "scipy_solution_norm": gauss_result["scipy_solution_norm"],
            "diff_solution_norm": gauss_result["diff_solution_norm"],
            "residual_norm": gauss_result["residual_norm"],
            "condition_number_custom": gauss_result["condition_number_custom"],
            "condition_number_scipy": gauss_result["condition_number_scipy"]
        })
    
    # Форматированный вывод таблицы
    print(f"{'Type':<20}{'My Norm':<15}{'Scipy Norm':<15}{'Diff Norm':<15}{'Residual':<15}{'Cond (Custom)':<15}")
    for result in results:
        print(f"{result['matrix_type']:<20}"
              f"{result['my_solution_norm']:<15.6e}"
              f"{result['scipy_solution_norm']:<15.6e}"
              f"{result['diff_solution_norm']:<15.6e}"
              f"{result['residual_norm']:<15.6e}"
              f"{result['condition_number_custom']:<15.6e}")

def main():
    while True:
        print("What do you want to do? (explore/solve/exit)")
        user_input = input().strip().lower()

        if user_input == "exit":
            break

        if user_input not in ["explore", "solve"]:
            print("Incorrect input. Please enter 'research', 'solve' or 'exit'")
            continue

        try:
            print("Enter matrix size (n):")
            n = int(input())
            
            print("Enter interval (default 100):")
            interval_input = input()
            interval = int(interval_input) if interval_input else 100

            validate_input(n, interval)

            if user_input == "explore":
                exploration(n, interval)
            elif user_input == "solve":
                print("Enter matrix type (random/hilbert/diagonal-dominant, default random):")
                matrix_type = input().strip().lower()
                if matrix_type not in ["random", "hilbert", "diagonal-dominant"]:
                    matrix_type = "random"

                matrix_generator = {
                    "random": generate_extended_matrix,
                    "hilbert": generate_hilbert_matrix,
                    "diagonal-dominant": generate_diagonal_dominant
                }[matrix_type]
                
                system = matrix_generator(n, interval)
                solution = gauss(system, n)

                custom = solution['custom_solution']
                scipy = solution['scipy_solution']
                print(f"\n{'Index':<6}{'Custom Solution':<25}{'Scipy Solution':<25}")
                for i, (custom_val, scipy_val) in enumerate(zip(custom, scipy), start=1):
                    print(f"{i:<6}{custom_val:<25.6e}{scipy_val:<25.6e}")
                
                print("\nSolution Norms:")
                print(f"{'My solution norm:':<25}{solution['my_solution_norm']:.6e}")
                print(f"{'Scipy solution norm:':<25}{solution['scipy_solution_norm']:.6e}")
                print(f"{'Difference norm:':<25}{solution['diff_solution_norm']:.6e}")
                print(f"{'Residual norm:':<25}{solution['residual_norm']:.6e}")
                print(f"{'Custom condition number:':<25}{solution['condition_number_custom']:.6e}")
                print(f"{'Scipy condition number:':<25}{solution['condition_number_scipy']:.6e}")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()