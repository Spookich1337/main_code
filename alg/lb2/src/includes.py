# Глобальная константа для представления бесконечности
global INF
INF = float('inf')

def tsp(graph, n, debug=False):
    """
    Точное решение задачи коммивояжера методом динамического программирования
    с использованием битовых масок.
    
    Параметры:
        graph - матрица смежности графа (n x n)
        n - количество городов
        debug - флаг отладочного вывода (по умолчанию False)
    
    Возвращает:
        tuple: (минимальная стоимость, список городов пути) или (INF, None) если путь не найден
    """
    
    # Инициализация таблицы динамического программирования
    size = 1 << n  # Всего возможных масок состояний (2^n)
    dp = [[INF] * n for _ in range(size)]  # Таблица минимальных стоимостей
    parent = [[-1] * n for _ in range(size)]  # Таблица для восстановления пути

    # Базовый случай: начало из города 0 (маска 000..001)
    dp[1][0] = 0  # Стоимость пути из 0 в 0 равна 0

    if debug:
        print("\n--- Начало алгоритма точного решения (метод динамического программирования) ---")
        print(f"Инициализирована таблица DP размером {size} x {n}")
        print(f"Начальное состояние: dp[1][0] = 0 (маска 000..001, город 0)")

    # Основной цикл динамического программирования
    for mask in range(size):
        if debug and mask % 100 == 0:  # Периодический вывод для больших n
            print(f"\nОбрабатываю маску: {bin(mask)}")
            
        for i in range(n):
            if dp[mask][i] == INF:  # Пропускаем непосещенные комбинации
                continue
                
            if debug:
                print(f"  Город {i}: текущая стоимость = {dp[mask][i]}")
                
            # Перебираем все возможные переходы
            for j in range(n):
                # Условия перехода:
                # - города разные
                # - город j еще не посещен в текущей маске
                # - существует ребро i->j
                if i != j and (mask & (1 << j)) == 0 and graph[i][j] > 0:
                    new_mask = mask | (1 << j)  # Новая маска с посещенным городом j
                    new_cost = dp[mask][i] + graph[i][j]  # Новая стоимость
                    
                    # Если нашли более оптимальный путь
                    if new_cost < dp[new_mask][j]:
                        if debug:
                            print(f"    Обновляю dp[{bin(new_mask)}][{j}]: {dp[new_mask][j]} -> {new_cost} (из города {i})")
                        dp[new_mask][j] = new_cost
                        parent[new_mask][j] = i  # Запоминаем предка для восстановления пути

    # Поиск минимального гамильтонова цикла
    full_mask = (1 << n) - 1  # Маска всех посещенных городов (111..111)
    min_cost = INF
    best_j = -1  # Будет хранить последний город перед возвратом в 0

    if debug:
        print("\n--- Поиск оптимального маршрута ---")
        print(f"Полная маска всех городов: {bin(full_mask)}")

    # Проверяем все возможные завершения цикла
    for j in range(n):
        if j != 0 and graph[j][0] > 0:  # Должен существовать путь из j в 0
            total = dp[full_mask][j] + graph[j][0]  # Полная стоимость цикла
            if debug:
                print(f"  Город {j}: стоимость полного цикла = {total} (dp[{bin(full_mask)}][{j}] = {dp[full_mask][j]} + graph[{j}][0] = {graph[j][0]})")
            if total < min_cost:
                min_cost = total
                best_j = j

    # Восстановление пути
    if min_cost == INF:
        if debug:
            print("Не найден допустимый маршрут")
        return INF, None
    else:
        path = []
        current = best_j
        current_mask = full_mask
        
        if debug:
            print(f"\nВосстановление пути (начало с города {current}, маска {bin(current_mask)})")
            
        # Обратный проход от конечного города к начальному
        while current != 0:
            path.append(current)
            prev = parent[current_mask][current]
            if debug:
                print(f"  Текущий город: {current}, предыдущий: {prev}, маска: {bin(current_mask)}")
            current_mask ^= (1 << current)  # Удаляем текущий город из маски
            current = prev
            
        path.append(0)  # Добавляем начальный город в конец
        path = path[::-1]  # Разворачиваем путь (чтобы шел от 0)
        path.append(0)  # Добавляем возврат в начальный город для завершения цикла
        
        if debug:
            print(f"Финальный путь: {path}, стоимость: {min_cost}")
        return min_cost, path
    

def approx(graph, start_city=0, debug=False):
    """
    Приближенное решение задачи коммивояжера методом ближайшего соседа
    с последующей оптимизацией 2-opt.
    
    Параметры:
        graph - матрица смежности графа (n x n)
        start_city - начальный город (по умолчанию 0)
        debug - флаг отладочного вывода (по умолчанию False)
    
    Возвращает:
        tuple: (список городов пути, стоимость) или ("no path", 0) если путь не найден
    """
    
    n = len(graph)
    if n == 0:
        if debug:
            print("Граф пуст")
        return "no path", 0
    
    # Проверка на существование исходящих путей из стартового города
    if all(graph[start_city][j] <= 0 for j in range(n) if j != start_city):
        if debug:
            print(f"Нет исходящих путей из стартового города {start_city}")
        return "no path", 0

    if debug:
        print("\n--- Начало приближенного алгоритма (метод ближайшего соседа с оптимизацией 2-opt) ---")
        print(f"Стартовый город: {start_city}")

    # Алгоритм ближайшего соседа с фиксированным стартом
    def nearest_neighbor(start):
        """Построение начального маршрута методом ближайшего соседа"""
        path = [start]
        visited = set([start])
        total_cost = 0
        
        current = start
        for step in range(n - 1):  # Нужно посетить n-1 оставшихся городов
            if debug:
                print(f"\nШаг {step+1}: текущий город {current}, посещенные города: {visited}")
                
            next_node = -1
            min_dist = float('inf')
            
            # Поиск ближайшего непосещенного города
            for j in range(n):
                if j not in visited and graph[current][j] > 0 and graph[current][j] < min_dist:
                    min_dist = graph[current][j]
                    next_node = j
                    
            if next_node == -1:  # Если не нашли подходящий город
                if debug:
                    print("Не найден следующий город - маршрут прерван")
                return None, float('inf')
                
            path.append(next_node)
            visited.add(next_node)
            total_cost += min_dist
            if debug:
                print(f"  Выбран город {next_node} (расстояние {min_dist}), общая стоимость: {total_cost}")
            current = next_node
        
        # Попытка вернуться в стартовый город
        if graph[current][start] > 0:
            total_cost += graph[current][start]
            path.append(start)
            if debug:
                print(f"\nВозврат в стартовый город {start} (расстояние {graph[current][start]})")
                print(f"Исходный маршрут: {path}, общая стоимость: {total_cost}")
            return path, total_cost
        else:
            if debug:
                print("\nНевозможно вернуться в стартовый город")
            return None, float('inf')

    # Построение начального маршрута
    path, cost = nearest_neighbor(start_city)

    if path is None:
        if debug:
            print("Не удалось построить маршрут методом ближайшего соседа")
        return "no path", 0

    # Оптимизация 2-opt (без изменения стартового города)
    def two_opt(path, cost):
        """Оптимизация маршрута методом 2-opt"""
        if debug:
            print("\n--- Начало оптимизации 2-opt ---")
            print(f"Начальный маршрут: {path}, стоимость: {cost}")
            
        improved = True
        iteration = 0
        
        while improved:
            iteration += 1
            improved = False
            
            # Перебираем все возможные пары ребер для перестановки
            # Не изменяем стартовый город (первый и последний элементы)
            for i in range(1, len(path) - 2):
                for j in range(i + 1, len(path) - 1):
                    # Текущие ребра: a-b и c-d
                    a, b, c, d = path[i-1], path[i], path[j], path[j+1]
                    
                    # Если перестановка дает улучшение
                    if graph[a][b] + graph[c][d] > graph[a][c] + graph[b][d]:
                        old_cost_segment = graph[a][b] + graph[c][d]
                        new_cost_segment = graph[a][c] + graph[b][d]
                        improvement = old_cost_segment - new_cost_segment
                        new_cost = cost - improvement
                        
                        if debug:
                            print(f"\nИтерация {iteration}: улучшение найдено на сегменте {i}-{j}")
                            print(f"  Старый сегмент: {a}-{b} ({graph[a][b]}) + {c}-{d} ({graph[c][d]}) = {old_cost_segment}")
                            print(f"  Новый сегмент: {a}-{c} ({graph[a][c]}) + {b}-{d} ({graph[b][d]}) = {new_cost_segment}")
                            print(f"  Улучшение: {improvement}, новая стоимость: {new_cost}")
                            
                        # Переворачиваем подотрезок пути между i и j
                        path[i:j+1] = path[i:j+1][::-1]
                        cost = new_cost
                        improved = True
                        
                        if debug:
                            print(f"  Новый маршрут: {path}")
                            
        if debug:
            print(f"\nЗавершено после {iteration} итераций")
            print(f"Оптимизированный маршрут: {path}, стоимость: {cost}")
        return path, cost

    # Применяем оптимизацию 2-opt
    optimized_path, optimized_cost = two_opt(path, cost)

    if optimized_cost == float('inf'):
        if debug:
            print("Оптимизированный маршрут недействителен")
        return "no path", 0
    else:
        if debug:
            print(f"\nФинальный результат:")
            print(f"Маршрут: {optimized_path}")
            print(f"Общая стоимость: {optimized_cost}")
        return optimized_path, optimized_cost