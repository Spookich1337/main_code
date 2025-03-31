#include <iostream>
#include <vector>
#include <string>

// Функция для вычисления префикс-функции (pi-функции)
std::vector<int> computePrefixFunction(const std::string& pattern) {
    std::cout << "-----------------------------\n";
    std::cout << "Calculating prefix function for pattern: " << pattern << '\n';
    int m = pattern.size();
    std::vector<int> pi(m, 0);
    int j = 0;

    for (int i = 1; i < m; i++) {
        while (j > 0 && pattern[i] != pattern[j]) {
            j = pi[j - 1];
        }
        if (pattern[i] == pattern[j]) {
            j++;
        }
        pi[i] = j;
        std::cout << "pi[" << i << "] = " << pi[i] << '\n';
    }
    std::cout << "Ready prefix: ";
    for (int x : pi) std::cout << x << " ";
        std::cout <<"\n-----------------------------\n";
    return pi;
}

// Функция КМП
std::vector<int> KMPsearch(const std::string& text, const std::string& pattern) {
    int n = text.size(), m = pattern.size();
    std::vector<int> pi = computePrefixFunction(pattern);
    std::vector<int> result;  // Индексы вхождений шаблона в текст
    
    int j = 0; // Указатель на pattern
    std::cout << "-----------------------------\n";
    std::cout << "Start finding " << pattern << " in " << text << '\n';
    for (int i = 0; i < n; i++) {
        while (j > 0 && text[i] != pattern[j]) {
            std::cout << "Mismatch: " << text[i] << " != " << pattern[j]  << ", rollback j = " << pi[j - 1] << '\n';
            j = pi[j - 1]; // Откат
        }
        if (text[i] == pattern[j]) {
            j++; // Совпадение продолжается
            std::cout << "Match: " << text[i] << " (i=" << i << ", j=" << j << ")" << '\n';
        }
        if (j == m) { // Полное совпадение
            std::cout << "Find on index " << i - m + 1 << '\n';
            result.push_back(i - m + 1);
            j = pi[j - 1]; // Продолжаем поиск
        }
    }
    std::cout << "-----------------------------\n";
    return result;
}

int main(int argc, char* argv[]) {
    if (argc == 0) {
        std::cout << "No arguments provided." << '\n';
        return 0;
    }

    std::string A, B;
    std::cin >> A >> B;

    std::vector<int> matches;

    std::string arg = argv[1];
    if (arg== "--first") {
        matches = KMPsearch(B, A);

        if (matches.size() == 0){
            std::cout << -1 << '\n';
        }else{
            std::string out;
            for (int pos : matches) {
                out += std::to_string(pos);
                out += ",";
            }
            out.pop_back();
            std::cout << out <<'\n';
        }
        return 0;
    }

    if (arg == "--second") {
        if (A.size() != B.size()) {
            std::cout << -1 << '\n';
            return 0;
        }

        std::string AA = A + A; // Дублируем строку A
        matches = KMPsearch(AA, B); // Ищем B в A+A

        if (matches.size() != 0) {
            std::cout << matches[0] << '\n';
        }else{
            std::cout << -1 << '\n';
        }
        return 0;
    }
    return 0;
}
