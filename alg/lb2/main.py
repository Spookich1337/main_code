# Импорт модуля с реализацией алгоритмов
import src.includes as inc

# Основной цикл программы для взаимодействия с пользователем
while True:
    # Запрос типа решения у пользователя
    print("Input type of solution (tsp/approx/exit)")
    user_input = input().strip().lower()  # Приводим к нижнему регистру и убираем пробелы

    # Выход из программы
    if user_input == "exit":
        break  # Прерываем цикл while

    # Запрос режима отладки
    print("Use debug? (y/n)")
    debug_input = input().strip().lower()
    debug = debug_input != "n"  # debug=True для любого ввода, кроме 'n'

    # Обработка точного решения (метод динамического программирования)
    if user_input == "tsp":
        print("Set size")
        try:
            n = int(input())  # Получаем размер матрицы
            if n <= 0:
                print("Size must be positive integer")
                continue
                
            # Ввод матрицы смежности
            print(f"Input {n}x{n} matrix (row by row, values separated by spaces):")
            graph = []
            valid_matrix = True
            
            for _ in range(n):
                row = list(map(int, input().split()))
                if len(row) != n:
                    print(f"Error: expected {n} values, got {len(row)}")
                    valid_matrix = False
                    break
                graph.append(row)
                
            if not valid_matrix:
                continue  # Возвращаемся к началу цикла при ошибке ввода
                
            # Вызов точного алгоритма
            cost, path = inc.tsp(graph, n, debug)
            
            # Вывод результатов
            if cost == inc.INF:
                print("No valid path exists")
            else:
                print(f"Minimum cost: {cost}")
                print("Optimal path:")
                print(" → ".join(map(str, path)))
                
        except ValueError:
            print("Invalid input - please enter integers only")
            continue

    # Обработка приближенного решения (метод ближайшего соседа + 2-opt)
    elif user_input == "approx":
        print("Set size")
        try:
            n = int(input())
            if n <= 0:
                print("Size must be positive integer")
                continue
                
            # Запрос стартового города
            print("Set start city (default=0):")
            start_input = input().strip()
            start = 0 if start_input == "" else int(start_input)
            
            # Проверка корректности стартового города
            if start < 0 or start >= n:
                print(f"Start city must be in range 0-{n-1}")
                continue
                
            # Ввод матрицы смежности
            print(f"Input {n}x{n} matrix (row by row, values separated by spaces):")
            graph = []
            valid_matrix = True
            
            for _ in range(n):
                row = list(map(int, input().split()))
                if len(row) != n:
                    print(f"Error: expected {n} values, got {len(row)}")
                    valid_matrix = False
                    break
                graph.append(row)
                
            if not valid_matrix:
                continue
                
            # Вызов приближенного алгоритма
            path, cost = inc.approx(graph, start, debug)
            
            # Вывод результатов
            if path == "no path":
                print("No valid path exists")
            else:
                print(f"Approximate cost: {cost}")
                print("Constructed path:")
                print(" → ".join(map(str, path)))
                
        except ValueError:
            print("Invalid input - please enter integers only")
            continue

    # Обработка некорректного ввода
    else:
        print("Incorrect input, please try again")
        print("Available options: tsp, approx, exit")