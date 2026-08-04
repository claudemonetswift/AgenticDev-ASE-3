#include "ie_ir_parser.hpp"
#include <iostream>
#include <memory>

using namespace std;

int main() {
    
    V10Parser parser;

    V10Parser::Params param1 = {"opset1", "MVN"};

    shared_ptr<struct Node> result1 = parser.test(param1);

    if (!result1) {
        cout << "1: opsetIt == opsets.end()" << endl;
    }
    else {
        cout << "1: opsetIt != opsets.end()" << endl;
    }


    V10Parser::Params param2 = {"opset1", "ROIPooling"};

    shared_ptr<struct Node> result2 = parser.test(param2);

    if (!result2) {
        cout << "2: opsetIt == opsets.end()" << endl;
    }
    else {
        cout << "2: opsetIt != opsets.end()" << endl;
    }

    return 0;
}
