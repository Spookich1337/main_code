global INF
INF = float('inf')


def tsp(graph, n):
    size = 1 << n
    dp = [[INF] * n for _ in range(size)]
    parent = [[-1] * n for _ in range(size)]

    dp[1][0] = 0  # Начинаем с города 0

    for mask in range(size):
        for i in range(n):
            if dp[mask][i] == INF:
                continue
            for j in range(n):
                if i != j and (mask & (1 << j)) == 0 and graph[i][j] > 0:
                    new_mask = mask | (1 << j)
                    new_cost = dp[mask][i] + graph[i][j]
                    if new_cost < dp[new_mask][j]:
                        dp[new_mask][j] = new_cost
                        parent[new_mask][j] = i

    full_mask = (1 << n) - 1
    min_cost = INF
    best_j = -1

    for j in range(n):
        if j != 0 and graph[j][0] > 0:
            total = dp[full_mask][j] + graph[j][0]
            if total < min_cost:
                min_cost = total
                best_j = j

    if min_cost == INF:
        return INF, None
    else:
        path = []
        current = best_j
        current_mask = full_mask
        while current != 0:
            path.append(current)
            prev = parent[current_mask][current]
            current_mask ^= (1 << current)
            current = prev
        path.append(0)  # Добавляем начальный город в конец
        path = path[::-1]  # Разворачиваем путь
        path.append(0)  # Возвращаемся в начальный город
        return min_cost, path
    

def approx(graph, start_city=0):
    n = len(graph)
    if n == 0:
        return "no path", 0
    
    # Проверка на существование исходящих путей из стартового города
    if all(graph[start_city][j] <= 0 for j in range(n) if j != start_city):
        return "no path", 0

    # Алгоритм ближайшего соседа с фиксированным стартом
    def nearest_neighbor(start):
        path = [start]
        visited = set([start])
        total_cost = 0
        
        current = start
        for _ in range(n - 1):
            next_node = -1
            min_dist = float('inf')
            for j in range(n):
                if j not in visited and graph[current][j] > 0 and graph[current][j] < min_dist:
                    min_dist = graph[current][j]
                    next_node = j
            if next_node == -1:
                return None, float('inf')
            path.append(next_node)
            visited.add(next_node)
            total_cost += min_dist
            current = next_node
        
        # Возврат в стартовый город
        if graph[current][start] > 0:
            total_cost += graph[current][start]
            path.append(start)
            return path, total_cost
        else:
            return None, float('inf')

    # Запускаем алгоритм только для стартового города
    path, cost = nearest_neighbor(start_city)

    if path is None:
        return "no path", 0

    # Оптимизация 2-opt (без изменения стартового города)
    def two_opt(path, cost):
        improved = True
        while improved:
            improved = False
            # Не трогаем первый и последний элементы (стартовый город)
            for i in range(1, len(path) - 2):
                for j in range(i + 1, len(path) - 1):
                    a, b, c, d = path[i-1], path[i], path[j], path[j+1]
                    if graph[a][b] + graph[c][d] > graph[a][c] + graph[b][d]:
                        new_cost = cost - (graph[a][b] + graph[c][d]) + (graph[a][c] + graph[b][d])
                        path[i:j+1] = path[i:j+1][::-1]
                        cost = new_cost
                        improved = True
        return path, cost

    optimized_path, optimized_cost = two_opt(path, cost)

    if optimized_cost == float('inf'):
        return "no path", 0
    else:
        return optimized_path, optimized_cost