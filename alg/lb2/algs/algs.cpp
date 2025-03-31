#include "algs.h"

std::vector<int> exactTSP(const std::vector<std::vector<int>>& dist, int n, bool debug) {
    int start = 0;
    std::vector<std::vector<int>> dp(1 << n, std::vector<int>(n, INF));
    std::vector<std::vector<int>> parent(1 << n, std::vector<int>(n, -1));
    dp[1 << start][start] = 0;

    // Группировка масок по количеству битов
    std::vector<std::vector<int>> masks_by_bits(n + 1);
    for (int mask = 0; mask < (1 << n); ++mask)
        masks_by_bits[__builtin_popcount(mask)].push_back(mask);

    // Заполнение dp и parent
    for (int cnt = 1; cnt <= n; ++cnt) {
        if (debug) {
            std::cout << "Processing masks with " << cnt << " bits set:" << std::endl;
        }
        for (int mask : masks_by_bits[cnt]) {
            if (debug) {
                std::cout << "  Mask: " << mask << std::endl;
            }
            for (int last = 0; last < n; ++last) {
                if (!(mask & (1 << last)) || dp[mask][last] == INF) continue;
                if (debug) {
                    std::cout << "    Last city: " << last << ", current dp value: " << dp[mask][last] << std::endl;
                }
                for (int next = 0; next < n; ++next) {
                    if (mask & (1 << next)) continue;
                    if (dist[last][next] == 0) continue; // Пропускаем нулевые ребра
                    int new_mask = mask | (1 << next);
                    if (dp[mask][last] + dist[last][next] < dp[new_mask][next]) {
                        dp[new_mask][next] = dp[mask][last] + dist[last][next];
                        parent[new_mask][next] = last;
                        if (debug) {
                            std::cout << "      Updating dp[" << new_mask << "][" << next << "] to " << dp[new_mask][next] << std::endl;
                        }
                    }
                }
            }
        }
    }

    // Восстановление пути
    std::vector<int> result;
    int full_mask = (1 << n) - 1;
    int min_dist = INF;
    int last_city = -1;

    // Находим последний город перед возвращением в стартовый
    for (int last = 0; last < n; ++last) {
        if (last != start && dp[full_mask][last] != INF && dist[last][start] != 0) {
            int total_dist = dp[full_mask][last] + dist[last][start];
            if (total_dist < min_dist) {
                min_dist = total_dist;
                last_city = last;
            }
        }
    }

    if (last_city == -1) {
        // Если путь не найден, возвращаем пустой вектор
        return result;
    }

    // Добавляем длину пути в результат
    result.push_back(min_dist);

    // Восстанавливаем путь
    int current_mask = full_mask;
    int current_city = last_city;
    while (current_city != -1) {
        result.push_back(current_city);
        int prev_city = parent[current_mask][current_city];
        current_mask ^= (1 << current_city); // Убираем текущий город из маски
        current_city = prev_city;
    }

    // Реверсируем путь, чтобы он начинался со стартового города
    reverse(result.begin() + 1, result.end());

    return result;
}

// Приближенный алгоритм: АЛШ-2 (ближайший сосед)
std::vector<int> approxTSP(const std::vector<std::vector<int>>& dist, int n, bool debug) {
    int start = 0;
    std::vector<bool> visited(n, false);
    std::vector<int> path;
    int current = start;
    visited[current] = true;
    path.push_back(current);
    int total_dist = 0;

    for (int i = 1; i < n; ++i) {
        if (debug) {
            std::cout << "Current city: " << current << std::endl;
        }
        int next = -1, min_dist = INF;
        for (int j = 0; j < n; ++j) {
            if (!visited[j] && dist[current][j] != 0 && dist[current][j] < min_dist) {
                min_dist = dist[current][j];
                next = j;
            }
        }
        if (next == -1) {
            std::vector<int> result;
            return result;
        }
        total_dist += min_dist;
        current = next;
        visited[current] = true;
        path.push_back(current);
        if (debug) {
            std::cout << "  Next city: " << current << ", distance: " << min_dist << std::endl;
        }
    }

    // Возвращение в стартовый город
    if (dist[current][start] != 0) {
        total_dist += dist[current][start];
        path.push_back(start);
    } else {
        std::vector<int> result;
        return result;
    }

    // Вывод пути и длины
    std::vector<int> result = {total_dist};

    for (int city : path)
        result.push_back(city);

    return result;
}