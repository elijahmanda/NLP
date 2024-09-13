#include <iostream>
#include "regex_tokenizer.h"

using namespace std;

int main(int a, char** argv){
    RegexTokenizer tok;
    tok.add_pattern("\\w+", "word");
    
    string text = argv[1];
    tok.compile();
    vector<Token> toks = tok.tokenize(text);
    long int i = 0;
    for (const Token& token: toks){
        cout << i << ". Text: " << token.text << ", Entity: " << token.entity << ", Index: (" << token.start << ", " << token.end << ")\n";
        i++;
    }
    string rep = text_span_replace("How are you", "is", 4, 7);
    cout << rep << endl;
    return 0;
}