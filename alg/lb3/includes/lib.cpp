#include "lib.h"

std::string get_moves(const std::vector<std::vector<Cell>>& matrix, int n, int m){
    std::string sequence;
    int i = m, j = n;
    while (i > 0 || j > 0) {
        std::cout << "Index i: " << i << " j: " << j << '\n';
        std::cout << "Move: " << matrix[i][j].move << '\n';
        switch (matrix[i][j].move) {
            case 'M':
                sequence += 'M';
                i--; j--;
                break;
            case 'R':
                sequence += 'R';
                i--; j--;
                break;
            case 'I':
                sequence += 'I';
                j--;
                break;
            case 'D':
                sequence += 'D';
                i--;
                break;
        }
    }
    std::reverse(sequence.begin(), sequence.end());
    return sequence;
}

std::set<std::string> get_all_moves(const std::vector<std::vector<Cell>>& matrix, int n, int m){
    std::set<std::string> result;
    
    if (n == 0 && m == 0) {
        result.insert("");
        return result;
    }
    
    std::vector<std::pair<int, int>> moves;
    int min_cost = matrix[n][m].cost;
    
    // Проверяем все возможные ходы
    if (n > 0 && m > 0 && matrix[n-1][m-1].cost + (matrix[n][m].move == 'R' ? 1 : 0) == min_cost) {
        moves.emplace_back(n-1, m-1);
    }
    if (m > 0 && matrix[n][m-1].cost + 1 == min_cost) {
        moves.emplace_back(n, m-1);
    }
    if (n > 0 && matrix[n-1][m].cost + 1 == min_cost) {
        moves.emplace_back(n-1, m);
    }
    
    // Рекурсивно собираем все последовательности
    for (const auto& move_pair : moves) {
        char move = ' ';
        if (move_pair.first == n-1 && move_pair.second == m-1) {
            move = (matrix[n][m].move == 'M' ? 'M' : 'R');
        } else if (move_pair.first == n && move_pair.second == m-1) {
            move = 'I';
        } else if (move_pair.first == n-1 && move_pair.second == m) {
            move = 'D';
        }
        
        auto sub_moves = get_all_moves(matrix, move_pair.first, move_pair.second);
        for (const auto& sub_move : sub_moves) {
            result.insert(sub_move + move);
        }
    }
    
    return result;
}

void printMatrix(const std::vector<std::vector<Cell>>& matrix){
    for (const auto& row : matrix) {
        for (Cell val : row) {
            std::cout << val.cost << "/" << val.move << " ";
        }
        std::cout << std::endl;
    }
}

void demonstrate_transformation(const std::string& str1, const std::string& str2, const std::string& sequence){
    std::string current = str1;
    int pos1 = 0, pos2 = 0;
    
    std::cout << "Start:  " << current << "\n";
    
    for (size_t i = 0; i < sequence.size(); ++i) {
        char move = sequence[i];
        std::string step = current;
        
        switch (move) {
            case 'M':
                step[pos1] = step[pos1] ;
                pos1++;
                pos2++;
                break;
            case 'R':
                step[pos1] = str2[pos2];
                pos1++;
                pos2++;
                break;
            case 'I':
                step.insert(pos1, 1, str2[pos2]);
                pos2++;
                break;
            case 'D':
                step.erase(pos1, 1);
                break;
        }
        
        std::cout << "Step " << i+1 << " (" << move << "): " << step << "\n";
        current = step;
    }
    
    std::cout << "Result: " << current << "\n";
}

std::vector<std::vector<Cell>> Levenshtain(std::string str_1, std::string str_2, std::vector<int> flags){
    int rep = 1, ins = 1, del = 1;
    
    if (flags[1] == 1){
        std::cout << "Input costs of operations(replace/insert/delete)\n";
        std::cin >> rep >> ins >> del;
    }

    int m = str_1.size(), n = str_2.size();

    std::vector<std::vector<Cell>> dp(m + 1, std::vector<Cell>(n + 1));

    for (int i = 0; i <= m; i++) {
        dp[i][0] = Cell(i * del, 'D');  // Удаление всех символов из str_1
    }
    for (int j = 0; j <= n; j++) {
        dp[0][j] = Cell(j * ins, 'I');  // Вставка всех символов в str_2
    }

    if (flags[0] == 1){
        std::cout << "Initialized matrix\n";
        printMatrix(dp);
    }

    // Заполнение матрицы
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (str_1[i - 1] == str_2[j - 1]) {
                dp[i][j] = Cell(dp[i - 1][j - 1].cost, 'M');
                if (flags[0] == 1){
                    std::cout << "compared chars: " << str_1[i - 1] << " " << str_2[j - 1] << " " << dp[i][j].move << '\n';
                } 
            } else {
                Cell replace_cost = Cell(dp[i - 1][j - 1].cost + rep, 'R');
                Cell insert_cost = Cell(dp[i][j - 1].cost + ins, 'I');
                Cell delete_cost = Cell(dp[i - 1][j].cost + del, 'D');

                if (replace_cost.cost <= insert_cost.cost && replace_cost.cost <= delete_cost.cost) {
                    dp[i][j] = replace_cost;
                } else if (insert_cost.cost <= delete_cost.cost) {
                    dp[i][j] = insert_cost;
                } else {
                    dp[i][j] = delete_cost;
                }

                if (flags[0] == 1){
                    std::cout << "compared chars: " << str_1[i - 1] << " " << str_2[j - 1] << " " << dp[i][j].move << '\n';
                } 
            }
        }
    }

    if (flags[0] == 1){
        std::cout << "Result matrix:\n";
        // Если нужно посмотреть всю матрицу:
        printMatrix(dp);
    }

    // Вывод результата (минимальное расстояние)
    std::cout << dp[m][n].cost << std::endl;

    if (flags[0] == 1){
        std::cout << "All moves: ";
        // Вывод последоввательности действий
        std::cout << get_moves(dp, n, m) << '\n';
    }

    // Вывод всех последовательностей
    auto all_sequences = get_all_moves(dp, m, n);
    std::cout << "\nAll optimal sequences (" << all_sequences.size() << "):\n";
    for (const auto& seq : all_sequences) {
        std::cout << seq << "\n";
    }

    // Демонстрация преобразования
    if (!all_sequences.empty()) {
        std::cout << "\nDemonstrating transformation for sequence: " << *all_sequences.begin() << "\n";
        demonstrate_transformation(str_1, str_2, *all_sequences.begin());
    }

    return dp;
}