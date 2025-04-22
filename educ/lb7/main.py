import random
import scipy
import numpy as np
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Linear system solver and matrix condition analysis using method Gaussuian",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Example usage \n"
               "   Exploration mode:\n"
               "     python main.py --n <size-matrix> --precision <digit>\n"
               "     python main.py --n <size-matrix> --precision <digit> --interval <digit>\n"
               "   Solution mode:\n"
               "     python main.py --n <size-matrix> --precision <digit>\n"
               "     python main.py --n <size-matrix> --precision <digit> --type <matrix-type> \n"
               "     python main.py --n <size-matrix> --precision <digit> --type <matrix-type> --interval <digit>\n"
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    research_parser = subparsers.add_parser(
        'research',
        help="Compare matrix types and their conditioning"
    )

    research_parser.add_argument(
        "--n",
        type=int,
        required=True,
        help="Matrix dimension positive digit"
    )

    research_parser.add_argument(
        "--precision",
        type=int,
        required=True,
        help="Computational precision (decimal places)"
    )

    research_parser.add_argument(
        "--interval",
        type=int,
        required=False,
        default=100,
        help="Max random digit (default 100)"
    )

    gauss_parser = subparsers.add_parser(
        'solve',
        help = "Solve specific linear system"
    )

    gauss_parser.add_argument(
        "--n",
        type=int,
        required=True,
        help="Matrix dimension positive digit"
    )

    gauss_parser.add_argument(
        "--precision",
        type=int,
        required=True,
        help="Computational precision (decimal places)"
    )

    gauss_parser.add_argument(
        "--type",
        type=str,
        required=False,
        choices=["random", "hilbert", "diagonal-dominant"],
        default="random",
        help="Matrix type:\n"
             "  random - random matrix\n"
             "  hilbert - matrix Hilbert\n"
             "  diagonal-dominant - matrix diagonal-dominant\n"
             "  default (random)"

    )

    gauss_parser.add_argument(
        "--interval",
        type=int,
        required=False,
        default=100,
        help="Max random digit (default 100)"
    )
    return parser.parse_args()

def validate_input(args):
    if args.n < 3: raise ValueError("Matrix size must be above 3")
    if args.precision < 0: raise ValueError("Precision cannot be negative")
    if args.interval < 0 or args.interval > 1000000: raise ValueError("Interval must be above 0 or below 1000000")

def generate_extended_matrix(n, precision, interval):
    matrix = [[round(random.uniform(0, interval), precision) for _ in range(n)] for _ in range(n)]
    vectorB = [round(random.uniform(0, interval), precision) for _ in range(n)]
    return [matrix[i] + [vectorB[i]] for i in range(n)]

def generate_hilbert_matrix(n, precision, interval):
    # H_ij = 1 / i + j - 1 индексация с 1
    matrix = [[round(1 / (i + j - 1), precision) for j in range(1, n + 1)] for i in range(1, n + 1)]
    b = [round(random.uniform(0, interval), precision) for _ in range(n)]
    return [matrix[i] + [b[i]] for i in range(n)]

def generate_diagonal_dominant(n, precision, interval):
    # Генерируем обычную матрицу после делаем так чтобы условие a_ii >= оставшихся чисел в строке
    matrix = [[round(random.uniform(0, interval), precision) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        row_sum = sum([matrix[i][j] for j in range(n) if i != j])
        matrix[i][i] += round(row_sum, precision)
    b = [round(random.uniform(0, interval), precision) for _ in range(n)]
    return [matrix[i] + [b[i]] for i in range(n)]

def straight_elimination(n, matrix):
    row_count = n
    column_count = n + 1
    for pivot_column in range(n):
        # search max row in current column
        max_row = pivot_column
        for row in range(pivot_column + 1, row_count):
            if abs(matrix[row][pivot_column]) > abs(matrix[max_row][pivot_column]):
                max_row = row

        if abs(matrix[max_row][pivot_column]) == 0:
            raise ValueError("Система вырождена - ведущий элемент нулевой")
        # swap rows
        matrix[pivot_column], matrix[max_row] = matrix[max_row], matrix[pivot_column]

        # normalize lead row
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

def gauss(matrix, n, precision):
    A = [row[:-1] for row in matrix]
    b = [row[-1] for row in matrix]
    straight_elimination(n, matrix)
    my_solution = inverse_step(n, matrix)
    solution_scipy = scipy.linalg.solve(A, b)
    return {
        "custom_solution": [round(x, precision) for x in my_solution],
        "scipy_solution": [round(x, precision) for x in solution_scipy],
        "residual_norm": compute_residual_norm(A, my_solution, b),
        "condition_number_custom": round(compute_conditional_digit(A, my_solution, b), precision),
        "condition_number_scipy": round(np.linalg.cond(A), precision)
    }

def compute_residual_norm(A, x, b):
    # calculate A * x
    # residual = Ax - b
    # vector norm
    n = len(A)
    residual = [0.0] * n
    for i in range(n):
        Ax = sum(A[i][j] * x[j] for j in range(n))
        residual[i] = Ax - b[i]

    residual_norm = sum(r ** 2 for r in residual) ** 0.5
    b_norm = sum(b_i ** 2 for b_i in b) ** 0.5
    return residual_norm / b_norm

def compute_conditional_digit(A, x, b):
    # cond2(A) = norm(A) * norm(inv_A)
    A_inv = np.linalg.inv(A)
    norm_A = np.linalg.norm(A, ord=2)
    norm_A_inv = np.linalg.norm(A_inv, ord=2)
    return norm_A * norm_A_inv

def exploration(n, precision, interval):
    # Исследование обусловленности таблица матрицы Диагонально-преобладающей, Гилберта, Случайно сгенерированной
    names = ["Random", "Hilbert", "Diagonal-dominant"]
    generators = [
        generate_extended_matrix,
        generate_hilbert_matrix,
        generate_diagonal_dominant
    ]

    results = []
    for name, generator in zip(names, generators):
        matrix = generator(n, precision, interval)
        gauss_result = gauss(matrix, n , precision)
        results.append({
            "matrix_type" : name,
            "residual_norm": gauss_result["residual_norm"],
            "condition_number_custom": gauss_result["condition_number_custom"],
            "condition_number_scipy": gauss_result["condition_number_scipy"]
        })
    print(f"{'Matrix Type':<25}{'Residual Norm':<30}{'Cond Num (Custom)':<25}{'Cond Num (Scipy)'}")
    print("-" * 128)
    for result in results:
        print(f"{result['matrix_type']:<25}{result['residual_norm']:<30}{result['condition_number_custom']:<25}{result['condition_number_scipy']:<25}")

def main():
    args = parse_args()
    validate_input(args)
    if args.command == "research":
        exploration(args.n, args.precision, args.interval)
    elif args.command == "solve":
        matrix_generator = {
            "random": generate_extended_matrix,
            "hilbert": generate_hilbert_matrix,
            "diagonal-dominant": generate_diagonal_dominant
        }[args.type]
        system = matrix_generator(args.n, args.precision,args.interval)
        solution = gauss(system, args.n, args.precision)

        custom = solution['custom_solution']
        scipy = solution['scipy_solution']
        print(f"{'Index':<6}{'Custom Solution':<20}{'Scipy Solution':<20}")
        print("-" * 46)
        for i, (custom, scipy) in enumerate(zip(custom, scipy), start=1):
            print(f"x{i:<5}{str(custom):<25}{str(scipy):<30}")
        print("-" * 46)
        print(f"{'Residual norm:':<30}{solution['residual_norm']:.5e}")
        print(f"{'Custom condition number:':<30}{solution['condition_number_custom']:}")
        print(f"{'Scipy condition number:':<30}{solution['condition_number_scipy']:}")

if __name__ == "__main__":
    main()