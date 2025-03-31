#include<iostream>
#include<vector>
#include<string>

void printMatrix(const std::vector<std::vector<int>>& matrix) {
    for (const auto& row : matrix) {
        for (int val : row) {
            std::cout << val << " ";
        }
        std::cout << std::endl;
    }
}

int main(){
    std::string str_1, str_2;
    int rep, ins, del;

    std::cin >> rep >> ins >> del;
    std::cin >> str_1 >> str_2;

    int n = str_2.size(), m = str_1.size();

    std::vector<std::vector<int>> matrix(n + 1, std::vector<int>(m + 1));

    matrix[0][0] = 0;
    
    for (int i = 1; i < m + 1; i++) {
        matrix[0][i] = i * ins;
    }

    for (int i = 1; i < n + 1; i++) {
        matrix[i][0] = i * del;
    }

    for (int i = 1; i < m + 1; i++){
        for (int j = 1; j < n + 1; j ++){
            if (str_1[i - 1] == str_2[j - 1]) {
                matrix[i][j] = matrix[i-1][j-1];
            } else {
                matrix[i][j] = std::min(matrix[i-1][j-1], std::min(matrix[i][j-1], matrix[i-1][j])) + 1;
            }
        }
    }
    
    printMatrix(matrix);
    return 0;
}