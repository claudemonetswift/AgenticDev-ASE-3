#include "ie_ir_parser.hpp"
#include <iostream>
#include <memory>
#include <unordered_map>
#include <string>

using namespace std;

struct Node {
    Node() {}
    ~Node() {}
};

V10Parser::V10Parser() {
    opsets["opset1"] = "opset1";
    opsets["opset2"] = "opset2";
    opsets["opset3"] = "opset3";
    opsets["opset4"] = "opset4";
    opsets["opset5"] = "opset5";
    opsets["opset6"] = "opset6";
}

shared_ptr<struct Node> V10Parser::test(V10Parser::Params params) {
    XmlDeserializer visitor(opsets);
    return visitor.on_adapter(params);
}

bool V10Parser::XmlDeserializer::isDefaultOpSet(const string& version) {
    static char const* prefix = "opset";
    static size_t const prefixLen = strlen(prefix);
    return version.length() == prefixLen + 1 &&
        version.compare(0, prefixLen, prefix) == 0 &&
        version[prefixLen] >= '1' && version[prefixLen] <= '6';
}

shared_ptr<struct Node> V10Parser::XmlDeserializer::on_adapter(V10Parser::Params params) {
    return parse_function(params);
}

shared_ptr<struct Node> V10Parser::XmlDeserializer::createNode(V10Parser::Params& params) {
    
    static const unordered_map<string, string> creators;

    shared_ptr<struct Node> ngraphNode;

    auto opsetIt = opsets.find(params.version);

    if (isDefaultOpSet(params.version)) {
        auto creatorIt = creators.find(params.type);
        if (creatorIt != creators.end()) {
            auto const & creator = creatorIt->second;
            if (opsetIt == opsets.end()) {
                ngraphNode = make_shared<struct Node>();
            }
        }
    }
 
    if (!ngraphNode && opsetIt != opsets.end()) {
        auto const & type = params.type == "Const" ? "Constant" : params.type;
        if (params.version == "opset1") {
            if (type == "MVN" || type == "ROIPooling") {
                
                opsetIt = opsets.find("opset2");
                if (opsetIt == opsets.end()) {
                    cout << "Cannot create" << endl;
                    return ngraphNode;
                }
            }
        }
    }

    ngraphNode = make_shared<struct Node>();

    return ngraphNode;
}

shared_ptr<struct Node> V10Parser::XmlDeserializer::parse_function(V10Parser::Params params) {
    return createNode(params);
}
