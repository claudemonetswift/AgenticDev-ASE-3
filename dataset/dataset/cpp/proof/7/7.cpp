#include <iostream>
#include <memory>

struct IFunction {
    IFunction() {}
    ~IFunction() {}
};

std::string m_definition;
std::shared_ptr<IFunction> m_value;

bool isOptional() {
    return true;
}

std::string setValue(const std::string &value) {
    std::string error;

    if (isOptional() && value.empty()) {
        m_value = std::shared_ptr<IFunction>();
        m_definition = value;
        return error;
    }

    try {
        m_value = std::shared_ptr<IFunction>();
        m_definition = value;
    } catch (std::exception &e) {
        error = e.what();
    }
    
    return error;
}

int main() {
    std::string value = "";
    std::string error = setValue(value);
    std::cout << "error: " << error << std::endl;
    std::cout << "is empty: " << error.empty() << std::endl;
    return 0;
}
