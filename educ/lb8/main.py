import random
import scipy
import argparse
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def parse_args():
    parser = argparse.ArgumentParser(
        description="Linear system solver and iterations analysis using method Jacobi",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Example usage \n"
               "   Research mode:\n"
               "     python main.py --n <size-matrix> --epsilon 6\n"
               "     python main.py --n <size-matrix> --interval <digit> --epsilon 6\n"
               "   Solution mode:\n"
               "     python main.py --n <size-matrix> --epsilon 6\n"
               "     python main.py --n <size-matrix> --interval <digit> --epsilon 6\n"
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
        "--interval",
        type=int,
        required=False,
        default=100,
        help="Max random digit (default 100)"
    )

    research_parser.add_argument(
        "--epsilon",
        type=int,
        required=False,
        default=6,
        help="Last epsilon digit above 0 (default 6)"
    )

    jacobi_parser = subparsers.add_parser(
        'solve',
        help="Solve specific linear system"
    )

    jacobi_parser.add_argument(
        "--n",
        type=int,
        required=True,
        help="Matrix dimension positive digit"
    )

    jacobi_parser.add_argument(
        "--interval",
        type=int,
        required=False,
        default=10,
        help="Max random digit (default 10)"
    )

    jacobi_parser.add_argument(
        "--epsilon",
        type=int,
        required=True,
        help="Epsilon digit above 0"
    )
    return parser.parse_args()

def validate_input(args):
    if args.n < 3: raise ValueError("Matrix size must be above 3")
    if args.epsilon < 0: raise ValueError("Epsilon value must be above 0")
    if (args.command != "solve") and (args.command != "research"): raise ValueError("Command not found try python main.py --help")
    if args.interval < 0 or args.interval > 1000000: raise ValueError("Interval must be above 0 or below 1000000")

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

def convert_epsilon(digit_epsilon):
    return float(10 ** (-digit_epsilon))

def exploration(n, interval, digit_epsilon):
    iterations= []
    epsilons = []
    matrix, b = generate_diagonal_dominant(n, interval)
    residuals = []
    for i in range(1, digit_epsilon + 1):
        epsilon = convert_epsilon(i)
        approach, approaches, iteration = jacobi_solve(n, epsilon, matrix, b)
        residuals.append(compute_residual_norm(matrix, approach, b))
        epsilons.append(epsilon)
        iterations.append(iteration)

    for i in range(len(residuals)):
        print(f"Residual {residuals[i]:<10.2e} with epsilon {epsilons[i]}")
    plt.figure(figsize=(10, 6))
    plt.plot(epsilons, iterations, marker='o')
    plt.xscale("log")
    plt.xlabel("Точность (epsilon)")
    plt.ylabel("Количество итераций")
    plt.title(f"Сходимость метода Якоби при размере матрицы = {n}x{n}")
    plt.grid(True)
    plt.gca().yaxis.set_major_locator(MultipleLocator(1))
    plt.ylim(bottom=0)
    plt.show()


def main():
    args = parse_args()
    validate_input(args)
    if args.command == "research":
        exploration(args.n, args.interval, args.epsilon)
    elif args.command == "solve":
        matrix, b = generate_diagonal_dominant(args.n, args.interval)
        epsilon = convert_epsilon(args.epsilon)
        approach, approaches, iteration = jacobi_solve(args.n, epsilon, matrix, b)
        residual = compute_residual_norm(matrix, approach, b)
        scipy_solution = scipy.linalg.solve(matrix, b)
        print(f"{'Approach:':<20}{'Scipy':<15}{'Diff':<15}")
        max_display = 20
        format_epsilon = f".{args.epsilon + 2}f"
        for i in range(min(args.n, max_display)):
            diff = abs(approach[i] - scipy_solution[i])
            print("{:<15} {:<15} {:<15}".format(
                f"{approach[i]:{format_epsilon}}",
                f"{scipy_solution[i]:{format_epsilon}}",
                f"{diff:.2e}"
            ))
        print()
        print(f"Residual: {residual}")
        print(f"Iterations: {iteration}")

if __name__ == "__main__":
    main()