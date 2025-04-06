#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <string>

using namespace std;

struct TrieNode {
    unordered_map<char, TrieNode*> children; // Переходы
    TrieNode* suff_link = nullptr;           // Суффиксная ссылка
    TrieNode* output_link = nullptr;         // Выходная ссылка (для ускорения)
    int pattern_id = -1;                     // Номер образца (если терминал)
    bool is_terminal = false;                // Конец образца
};

class AhoCorasick {
private:
    TrieNode* root;
    vector<string> patterns;

    // Построение бора
    void buildTrie() {
        root = new TrieNode();
        for (int i = 0; i < patterns.size(); ++i) {
            TrieNode* node = root;
            for (char c : patterns[i]) {
                if (node->children.find(c) == node->children.end()) {
                    node->children[c] = new TrieNode();
                }
                node = node->children[c];
            }
            node->is_terminal = true;
            node->pattern_id = i;
        }
    }

    // Построение суффиксных ссылок (аналог fail-функции)
    void buildSuffixLinks() {
        queue<TrieNode*> q;
        root->suff_link = root;

        for (auto& [c, child] : root->children) {
            child->suff_link = root;
            q.push(child);
        }

        while (!q.empty()) {
            TrieNode* node = q.front();
            q.pop();

            for (auto& [c, child] : node->children) {
                TrieNode* suff = node->suff_link;
                while (suff != root && suff->children.find(c) == suff->children.end()) {
                    suff = suff->suff_link;
                }
                if (suff->children.find(c) != suff->children.end()) {
                    child->suff_link = suff->children[c];
                } else {
                    child->suff_link = root;
                }
                q.push(child);
            }

            // Выходная ссылка (для терминалов)
            if (node->suff_link->is_terminal) {
                node->output_link = node->suff_link;
            } else {
                node->output_link = node->suff_link->output_link;
            }
        }
    }

public:
    AhoCorasick(const vector<string>& patterns) : patterns(patterns) {
        buildTrie();
        buildSuffixLinks();
    }

    // Поиск всех вхождений в тексте
    vector<pair<int, int>> search(const string& text) {
        vector<pair<int, int>> matches;  // (позиция, номер образца)
        TrieNode* node = root;

        for (int i = 0; i < text.size(); ++i) {
            char c = text[i];
            // Пропускаем по суффиксным ссылкам, пока не найдём переход
            while (node != root && node->children.find(c) == node->children.end()) {
                node = node->suff_link;
            }
            if (node->children.find(c) != node->children.end()) {
                node = node->children[c];
            }
            // Проверяем терминальные узлы и выходные ссылки
            TrieNode* out = node;
            while (out != nullptr) {
                if (out->is_terminal) {
                    matches.emplace_back(i - patterns[out->pattern_id].size() + 1, out->pattern_id);
                }
                out = out->output_link;
            }
        }
        return matches;
    }
};

int main() {
   std::string text;

    std::cin >> text;

    int n;
    std::cin >> n;

    std::vector<std::string> sub_str;

    for(int i = 0; i < n; i++){
        std::string tmp;
        std::cin >> tmp;

        sub_str.push_back(tmp);
    }

    AhoCorasick solution(sub_str);

    std::vector<std::pair<int, int>> result = solution.search(text);

    for (auto zxc : result){
        std::cout << zxc.first << ' ' << zxc.second <<
    }

    return 0;
}