import re
from typing import List, Tuple

import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize


def detect_tense(sentence):
    """
    Detects the tense of a given sentence.
    Returns one of the following strings: "present", "past", "future", or "unknown".
    """
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)
    tense = "unknown"

    for i in range(len(tagged)):
        if tagged[i][1] in ("VBP", "VBZ"):
            tense = "present"
        elif tagged[i][1] in ("VBD", "VBN"):
            tense = "past"
        elif tagged[i][1] == "MD":
            tense = "future"
    return tense


def split_tokenize(text: str) -> List[str]:
    """Splits a string into tokens based on whitespace."""
    return text.split()


def regex_sentence_tokenize(text: str) -> List[str]:
    """Splits a string into sentences using regular expressions."""
    # Use regular expressions to split text into sentences
    pattern = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s')
    sentences = re.split(pattern, text)
    return sentences


def stem_word(word: str) -> str:
    """Applies a stemming algorithm to a word using NLTK."""
    nltk.download('snowball_data')
    stemmer = nltk.stem.snowball.SnowballStemmer('english')
    return stemmer.stem(word)


def lemmatize_wordnet(word: str) -> str:
    """Applies a lemmatization algorithm to a word using NLTK."""
    nltk.download('wordnet')
    lemmatizer = nltk.stem.WordNetLemmatizer()
    return lemmatizer.lemmatize(word)


def remove_stopwords(tokens: List[str], language: str = 'english') -> List[str]:
    """Removes stopwords from a list of tokens using NLTK."""
    nltk.download('stopwords')
    stop_words = set(nltk.corpus.stopwords.words(language))
    return [token for token in tokens if token not in stop_words]


if __name__ == "__main__":
    sents = [
        ("She walks to school every day.", 'present'),
        ("He ate a sandwich for lunch.", 'past'),
        ("I will go to the store tomorrow.", 'future')
    ]
    for sent, tense in sents:
        detected_tense = detect_tense(sent)
        print(sent, "Tense:", detected_tense, "Expected:", tense)
        interactive = input(
            "Interactive? y/n:").lower().strip() in ("y", "yes")
    while True and interactive:
        sent = input("> ")
        if sent.strip():
            print(detect_tense(sent))
        else:
            break
