#include <string>
#include <vector>


inline std::vector<std::pair<std::size_t, std::size_t>> missing_indexes(const std::vector<std::pair<std::size_t, std::size_t>>& indexes, std::size_t total);
inline std::string text_span_replace(const std::string& text, const std::string& replacement, std::size_t start, std::size_t end);
inline std::string get_substring(const std::string& text, const std::size_t start, const std::size_t end);


inline std::vector<std::pair<std::size_t, std::size_t>> missing_indexes(
    const std::vector<std::pair<std::size_t, std::size_t>>& indexes,
    std::size_t total
) {
    std::vector<std::pair<std::size_t, std::size_t>> missing;
    if (indexes.empty()) {
        missing.emplace_back(0, total);
        return missing;
    }
    
    //std::size_t last_index = 0;
    if (indexes[0].first > 0) {
        missing.emplace_back(0, indexes[0].first);
    }
    if (indexes.back().second < total) {
        missing.emplace_back(indexes.back().second, total);
    }

    for (std::size_t i = 0; i < indexes.size() - 1; ++i) {
        std::size_t first_end = indexes[i].second;
        std::size_t next_start = indexes[i + 1].first;
        if (next_start > first_end) {
            missing.emplace_back(first_end, next_start);
        }
    }

    std::sort(missing.begin(), missing.end());
    return missing;
}

inline std::string text_span_replace(const std::string& text, const std::string& replacement, std::size_t start, std::size_t end) {
    return get_substring(text, 0, start).append(replacement).append(get_substring(text, end, text.size()));
}

inline std::string get_substring(const std::string& text, const std::size_t start, const std::size_t end) {
    
    std::string temp_text = "";
    size_t inc = start;
    while (inc < end){
        temp_text += text[inc];
        inc++;
    }
    return temp_text;
}