#include "algs/algs.h"

int main(){

    std::cout << "Enter the size: " << std::endl;
    int size;
    std::cin  >> size;

    std::cout << "Enter the elements: " << std::endl;
    std::vector<std::vector<int>> matrix(size, std::vector<int>(size));
    for (int i = 0; i < size; i++){
        for (int j = 0; j < size; j++){
            std::cin >> matrix[i][j];
        }
    }

    std::cout << "What solution do you want to use?(exact/approx)" << std::endl;
    std::string input;
    std::cin >> input;

    std::cout << "Do you wanna see how work program?(yes/no)" << std::endl;
    std::string input2;
    std::cin >> input2;
    bool debug = false;
    if (input2 == "yes"){
        debug = true;
    }

    if(input == "exact"){
        std::vector<int> answer = exactTSP(matrix, size, debug);

        if (answer.empty()) {
            std::cout << "no path" << std::endl;
        }else{
            std::cout <<  answer[0] << std::endl;
            
            for (int i = 1; i < answer.size(); i ++){
                std::cout << answer[i] << " ";
            }
            
            std::cout << answer[1] << std::endl;
        } 
    }else if(input == "approx"){
        std::vector<int> answer = approxTSP(matrix, size, debug);

        if (answer.empty()) {
            std::cout << "no path" << std::endl;
        }else{
            std::cout <<  answer[0] << std::endl;
            
            for (int i = 1; i < answer.size(); i ++){
                std::cout << answer[i] << " ";
            }
        } 
    }else{
        std::cout << "Invalid solution type" << std::endl;
    }
    
    return 0;
}