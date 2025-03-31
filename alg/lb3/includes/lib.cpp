#include "lib.h"

std::string get_moves(const std::vector<std::vector<Cell>>& matrix, int n, int m){
    std::string sequence;
    int i = m, j = n;
    while (i > 0 || j > 0) {
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

void printMatrix(const std::vector<std::vector<Cell>>& matrix){
    for (const auto& row : matrix) {
        for (Cell val : row) {
            std::cout << val.cost << "/" << val.move << " ";
        }
        std::cout << std::endl;
    }
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

    return dp;
}