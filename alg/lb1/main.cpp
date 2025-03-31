#include <iostream>
#include <vector>
#include <tuple>
#include <ctime>
#include <string>
#include<gnuplot-iostream.h>

using namespace std;

class Field {
private:
    vector<vector<int>> map;
    int size;
    vector<tuple<int, int, int>> stack;
    int stack_size;

public:
    Field(int size) : size(size), stack_size(0) {
        map.resize(size, vector<int>(size, 0));
    }

    void print() {//вывести поле в термниал
        for (const auto &row : map) {
            for (int cell : row) {
                cout << cell << " ";
            }
            cout << '\n';
        }
    }

    bool place_square(int x, int y, int z) {//разместить новый квадрат
        if (can_place(x, y, z)) {
            stack.emplace_back(x, y, z);
            stack_size++;
            for (int i = 0; i < z; ++i) {
                for (int j = 0; j < z; ++j) {
                    map[y + i][x + j] = 1;
                }
            }
            return true;
        }
        return false;
    }

    bool can_place(int x, int y, int z) {//проверка на возможность разместить квадрат
        if (x + z > size || y + z > size) return false;
        for (int i = 0; i < z; ++i) {
            for (int j = 0; j < z; ++j) {
                if (map[y + i][x + j] != 0) return false;
            }
        }
        return true;
    }

    tuple<int, int, int> get_back() {//удаляет последний добавленный квадрат
        auto tmp = stack.back();
        stack.pop_back();
        remove_square(get<0>(tmp), get<1>(tmp), get<2>(tmp));
        stack_size--;
        return tmp;
    }

    void remove_square(int x, int y, int z) {//удаляет область
        for (int i = 0; i < z; ++i) {
            for (int j = 0; j < z; ++j) {
                map[y + i][x + j] = 0;
            }
        }
    }

    tuple<int, int> is_full() {//проверяет заполнен ли квадрат
        for (int x = 0; x < size; ++x) {
            for (int y = 0; y < size; ++y) {
                if (map[y][x] == 0) return {x, y};
            }
        }
        return {-1, -1};
    }

    vector<tuple<int, int, int>> get_stack() { return stack; }
};

vector<tuple<int, int, int>> for_2(int n, bool flag) { // оптимизация для квадратов со стороной четной 2
    if (flag == true) {
        cout << "using optimization for % 2\n";
    }
    vector<tuple<int, int, int>> answer = {
        {0, 0, n / 2}, {0, n / 2, n / 2}, {n / 2, 0, n / 2}, {n / 2, n / 2, n / 2}};
    return answer;
}

vector<tuple<int, int, int>> for_3(int n, bool flag) {// оптимизация для квадратов со стороной четной 3
    if (flag == true) {
        cout << "using optimization for % 3\n";
    }
    vector<tuple<int, int, int>> answer = {
        {0, 0, n / 3}, {0, n / 3, n / 3}, {0, 2 * (n / 3), n / 3},
        {n / 3, 0, n / 3}, {2 * (n / 3), 0, n / 3}, {n / 3, n / 3, 2 * (n / 3)}};
    return answer;
}

vector<tuple<int, int, int>> backtracking(int n, bool flag) {
    if (n % 2 == 0) {
        return for_2(n, flag);
    } else if (n % 3 == 0) {
        return for_3(n, flag);
    }else{
        Field field(n);

        if (flag == true) {
            cout << "using optimization for simple number\n";
        }

        //оптимизация для простых чисел 
        field.place_square(n / 2, n / 2, n / 2 + 1);
        field.place_square(n - n / 2, 0, n / 2);
        field.place_square(0, n - n / 2, n / 2);

        //создаем стек состояний столешниц
        vector<vector<tuple<int, int, int>>> stack_of_fields = {field.get_stack()};
        
        //создаем вектор содержащий лучшее решение и флаг макссимального кол-во кусков столешницы
        vector<tuple<int, int, int>> result;
        int result_flag = 3 + n + 1;

        while (!stack_of_fields.empty()) {
            //берем из стека последнее состояние столешницы
            Field main_field(n);
            vector<tuple<int, int, int>> last_stack = stack_of_fields.back();
            stack_of_fields.pop_back();
            for (const auto &s : last_stack) {
                main_field.place_square(get<0>(s), get<1>(s), get<2>(s));
            }

            if (flag == true) {
                cout << "main field\n";
                main_field.print();
            }

            //проверяем заполнена ли столешница 
            auto [x, y] = main_field.is_full();
            if (x == -1 && y == -1) {
                if (flag == true) {
                    cout << "save optimal solution\n";
                }
                result = main_field.get_stack();
                result_flag = result.size();
            }

            if (x != -1 && y != -1 && flag == true) {
                cout << "empty place: " << x + 1 << " " << y + 1 << "\n";
            }

            //оптимизация пропуска неоптимальных решений
            if (main_field.get_stack().size() + 1 >= result_flag) {
                if (flag == true){
                    cout << "skip, not optimal solution\n";
                    cout << "----------------------------------------\n";
                }
                continue;
            }

            for (int i = 1; i < n - 1; ++i) {
                if (main_field.can_place(x, y, i)) {
                    //создаем копию  основного поля
                    Field tmp_field(n);
                    for (const auto &s : main_field.get_stack()) {
                        tmp_field.place_square(get<0>(s), get<1>(s), get<2>(s));
                    }
                    
                    //помещаем на нее новый квадрат
                    tmp_field.place_square(x, y, i);

                    if (flag == true) {
                        cout << "place new square\n";
                        cout << "x: " << x + 1 << ", y: " << y + 1 << ", i: " << i << ", count squares:" << tmp_field.get_stack().size() << '\n';
                        tmp_field.print();
                    }

                    //сохраняем его в стек
                    stack_of_fields.push_back(tmp_field.get_stack());
                } else {
                    break;
                }
            }
            cout << "----------------------------------------\n";
        }
        return result;
    }
}

void test() {
    std:: vector<int> vectN = {3, 5, 6, 7, 9, 10, 11};
    std:: vector<int> expectedMinCountSquares = {6, 8, 4, 9, 6, 4, 11};
    for (int i = 0; i < vectN.size(); i++) {
        vector<tuple<int, int, int>> answer = backtracking(vectN[i], false);
        assert(answer.size() == expectedMinCountSquares[i]);
    }
    std:: cout << "Success!" << std:: endl;
}

void graphic() {
    Gnuplot gp;

    gp << "set title 'график функции backtracking'" << std::endl;
    gp << "set xlabel 'размер'" << std::endl;
    gp << "set ylabel 'время'" << std::endl;
    gp << "plot '-' with lines" << std::endl;

    vector<int> simple_numbers = {1,2,3,5,7,11,13,17,19};

    for (int i = 0; i < simple_numbers.size(); i++) {
        clock_t start = clock();
        backtracking(simple_numbers[i], false);
        clock_t end = clock();

        gp << simple_numbers[i] << " " << (double)(end - start) / CLOCKS_PER_SEC << std::endl;
    }
    gp << "e" << std::endl;
}

void check() {
    int n;
    cout << "input size of table\n";
    cin >> n;

    bool flag = false;
    cout << "vision?\n";
    string input;
    cin >> input;
    if (input == "yes") {
        flag = true;
    } else {
        flag = false;
    }

    clock_t start = clock();
    vector<tuple<int, int, int>> answer = backtracking(n, flag);
    clock_t end = clock();

    cout << "time: " << (end - start) / (double) CLOCKS_PER_SEC << '\n';
    cout << answer.size() << '\n';
    for (auto i : answer) {
        cout << get<0>(i) + 1 << " " << get<1>(i) + 1 << " " << get<2>(i) << '\n';
    } 
}

int main() {
    int command;
    cout << "what do you wanna see? 1 - standart usage, 2 - graphic, 3 - test" << endl;
    cin >> command;

    if (command == 1) {
        check();
    } else if (command == 2) {
        graphic();
    } else {
        test();
    }
}