#include "includes/lib.h"

int main() {
    std::cout << "Input strings\n";

    std::string str_1, str_2;
    std::cin >> str_1 >> str_2;

    std::string input;
    std::vector<int> flags(2, 0);

    std::cout << "Wanna see how program works?(y/n)\n";
    std::cin >> input;
    if (input == "y"){
        flags[0] = 1;
    }

    input = "";
    std::cout << "Wanna use your own costs of operation?(y/n)\n";
    std::cin >> input;
    if (input == "y"){
        flags[1] = 1;
    }

    Levenshtain(str_1, str_2, flags);

    return 0;
}