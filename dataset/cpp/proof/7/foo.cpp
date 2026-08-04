#include <memory>
#include <string>
#include <stdexcept>
#include <iostream>

class IFunction {
    public:
        IFunction(int x) { if (x > 1) { throw std::runtime_error(""); } }
        //IFunction* allocate(std::size_t) { throw std::bad_alloc(); }
}; 

int main() {

    std::string error;
    try {
        auto foo = std::shared_ptr<IFunction>(new IFunction(2));
    } catch (std::exception &e) {
        error = e.what();
        std::cout << error << std::endl;
    }

}


