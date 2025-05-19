from collections import deque

def bfs(capacity, flow, s, t, parent):
    n = len(capacity)
    visited = [False] * n
    queue = deque()
    queue.append(s)
    visited[s] = True

    while queue:
        u = queue.popleft()
        for v in range(n):
            if not visited[v] and capacity[u][v] - flow[u][v] > 0:
                parent[v] = u
                visited[v] = True
                queue.append(v)
                if v == t:
                    return True
    return False

def ford_fulkerson(capacity, s, t):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    parent = [-1] * n
    max_flow = 0
    step = 0

    while bfs(capacity, flow, s, t, parent):
        # Находим минимальную пропускную способность вдоль пути
        path_flow = float('inf')
        v = t
        path = []
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, capacity[u][v] - flow[u][v])
            path.append((u, v))
            v = u
        path.reverse()

        # Добавляем поток по найденному пути
        v = t
        while v != s:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow  # остаточная сеть
            v = u

        max_flow += path_flow
        step += 1

        # Печать промежуточных данных
        print(f"\nШаг {step}:")
        print(f"  Найден путь: {path}")
        print(f"  Поток по пути: {path_flow}")
        print(f"  Обновлённая матрица потока:")
        for row in flow:
            print(row)

    print(f"\nМаксимальный поток: {max_flow}")
    return max_flow

# Пример
INF = float('inf')
capacity = [
#   A  B  C  D  E  F  G  H  I  J  K
    [ 0,12,20, 9, 0, 0, 0, 0, 0, 0, 0],  # A (0)
    [ 0, 0, 0, 0,10, 4, 0, 0, 0, 0, 0],  # B (1)
    [ 0, 0, 0, 0, 8, 6, 0, 0, 0, 0, 0],  # C (2)
    [ 0, 0, 0, 0, 0, 1, 8, 0, 0, 0, 0],  # D (3)
    [ 0, 0, 0, 0, 0, 0, 0, 5, 7, 0, 0],  # E (4)
    [ 0, 0, 0, 0, 0, 0, 0, 0, 6, 8, 0],  # F (5)
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 9],  # G (6)
    [ 0, 0, 0, 0, 0, 0, 0, 0,15, 0, 0],  # H (7)
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,21],  # I (8)
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,21],  # J (9)
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # K (10)
]

source = 0
sink = 11
ford_fulkerson(capacity, source, sink)
