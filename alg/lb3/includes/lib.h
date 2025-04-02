#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <set>

class Cell{
    public:
    int cost;
    char move;

    Cell() : cost(0), move('\0') {}

    Cell(int new_cost, char new_move): cost(new_cost), move(new_move) {} 

};


std::set<std::string> get_all_moves(const std::vector<std::vector<Cell>>& matrix, int i, int j);

std::string get_moves(const std::vector<std::vector<Cell>>& matrix, int n, int m);

void printMatrix(const std::vector<std::vector<Cell>>& matrix);

void demonstrate_transformation(const std::string& str1, const std::string& str2, const std::string& sequence);

std::vector<std::vector<Cell>> Levenshtain(std::string str_1, std::string str_2, std::vector<int> flags);