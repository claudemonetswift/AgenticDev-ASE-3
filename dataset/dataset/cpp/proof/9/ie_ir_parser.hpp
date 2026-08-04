#ifndef parser_H_
#define parser_H_

#include <unordered_map>
#include <string>
#include <memory>

using namespace std;

class V10Parser {

    public:
        struct Params {
            string version;
            string type;
        };

        V10Parser(); 
                
        shared_ptr<struct Node> test(V10Parser::Params params); 

    private:
        unordered_map<string, string> opsets;

        class XmlDeserializer {

            public:
                XmlDeserializer(const unordered_map<string, string>& opsets) : opsets(opsets) {}

                shared_ptr<struct Node> on_adapter(V10Parser::Params params);
    
            private:
                const unordered_map<string, string>& opsets;

                bool isDefaultOpSet(const string& version);
        
                shared_ptr<struct Node> createNode(V10Parser::Params& params);

                shared_ptr<struct Node> parse_function(V10Parser::Params params);

        };
};

#endif
