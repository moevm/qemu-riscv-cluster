#include <iostream>
#include <chrono>
#include <thread>

int main(){
    for(int i = 0; i < 5; ++i){
        std::cout << "Hello Docker!(" << i << ")" << std::endl;
        std::cerr << "Error message!(" << i << ")" << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    return 0;
}