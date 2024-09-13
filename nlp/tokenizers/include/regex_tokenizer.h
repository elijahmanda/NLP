#ifndef LIB_REGEX_TOKENIZER
#define LIB_REGEX_TOKENIZER

#include <iostream>
#include <string>
#include <regex>
#include <vector>
#include <tuple>
#include <set>
#include <algorithm>
#include <cassert>

#include "utils.h"



using PatternsT = std::vector<std::tuple<std::string, std::string>>;
using RegexOptionType = std::regex_constants::syntax_option_type;

RegexOptionType IGNORECASE = std::regex_constants::icase;
RegexOptionType OPTIMIZE = std::regex_constants::optimize;
RegexOptionType ECMASCRIPT = std::regex_constants::ECMAScript;
    

struct Token {
    std::string text;
    std::string entity;
    std::size_t start;
    std::size_t end;
};

class RegexTokenizer {
    
public:

    std::vector<std::tuple<std::regex, std::string>> _compiled_patterns;
    PatternsT _patterns;
    bool _compiled = false;
    RegexOptionType _flags = OPTIMIZE;
    
    RegexTokenizer(){};
    
    bool is_compiled() {
        return _compiled;
    }
    
    void _compile(bool sort) {
        if (sort) {
            std::sort(
                _patterns.begin(),
                _patterns.end(),
                [](const auto& a, const auto& b) {
                    return std::get<0>(a).length() > std::get<0>(b).length();
            });
        }
        _compiled_patterns.clear();
        for (const auto& entry : _patterns) {
            std::string pattern_str = std::get<0>(entry);
            std::string entity = std::get<1>(entry);
            std::regex pattern(pattern_str.c_str(), _flags);
            _compiled_patterns.emplace_back(pattern, entity);
        }
        _compiled = true;
    }
    
    std::vector<Token> _merge_non_entity_tokens(const std::string& text, std::vector<Token>& tokens) {
        
        std::vector<std::pair<std::size_t, std::size_t>> indexes;
        for (const auto& token : tokens) {
            indexes.push_back(std::make_pair(token.start, token.end));
        }
        auto missing = missing_indexes(indexes, text.size());
        for (const auto& index : missing) {
            Token token;
            token.text = get_substring(text, index.first, index.second);
            token.entity = "";
            token.start = index.first;
            token.end = index.second;
            tokens.emplace_back(token);
        }
        return tokens;
    }
    
    void compile(bool ignorecase=false, bool sort = false) {
        if (!_compiled){
            if (ignorecase){
                _flags |= IGNORECASE;
            }
            _compile(sort);
        }
    }

    std::vector<Token> tokenize(const std::string& text, bool merge = false) {
        std::string original_text = text;
        if (!_compiled) {
            compile();
        }
        std::vector<Token> tokens;
        std::string temp_text = text;
        for (const auto& [compiled_pattern, entity] : _compiled_patterns) {
            for (std::sregex_iterator it(temp_text.begin(), temp_text.end(), compiled_pattern), end_it; it != end_it; ++it) {
                size_t start = it->position();
                size_t end = start + it->length();
                Token token;
                token.text = it->str();
                token.entity = entity;
                token.start = start;
                token.end = end;
                tokens.emplace_back(token);
                temp_text = text_span_replace(std::string(temp_text), std::string(end - start, ' '), start, end);
                //std::cout << "Temp: " << temp_text << "\n";
            }
        }
        if (merge) {
            tokens = _merge_non_entity_tokens(original_text, tokens);
        }
        
        std::sort(tokens.begin(), tokens.end(), [](const Token& a, const Token& b) {
            return a.start < b.start;
        });
        
        /*for (const Token& token: tokens){
            std::cout << "Text: " << token.text << ", Entity: " << token.entity << ", Index: (" << token.start << ", " << token.end << ")\n";
        }*/
        return tokens;
    }

    void add_pattern(const std::string& pattern, const std::string& entity) {
        assert(!_compiled);
        _patterns.emplace_back(pattern, entity);
    }

    void clear() {
        _patterns.clear();
        _compiled_patterns.clear();
        _compiled = false;
        _flags = OPTIMIZE;
    }

    std::vector<std::string> get_entities(){
        std::set<std::string> entities_set;
        for (const auto& entry : _patterns) {
            entities_set.insert(std::get<1>(entry));
        }
        std::vector<std::string> entities(entities_set.begin(), entities_set.end());
        std::sort(entities.begin(), entities.end());
        return entities;
    }

    std::size_t get_pattern_count() const {
        return _patterns.size();
    }

    std::size_t get_entity_count() {
        return get_entities().size();
    }
    
    
};

#endif