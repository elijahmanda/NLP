from nlp.tokenizers.regex_tokenizer import RegexTokenizer, FastRegexTokenizer

from nlp.utils.timer import timer
import pprint as pp


PATTERNS = [
    ("digit", r"\d+"),
    ("word", r"\w+")
]
TEXT = open("test.txt").read() * 5
print("Testing on text of length %s" % len(TEXT))


py = RegexTokenizer()
py.set_patterns(PATTERNS, False)
py.compile("(?m)")
rust = FastRegexTokenizer()
rust.set_patterns(PATTERNS, False)
rust.compile("(?m)")


@timer()
def test_rust():

    tokens = rust.tokenize(TEXT)
    print("%d tokens" % len(tokens))
    return tokens


@timer()
def test_py():

    tokens = py.tokenize(TEXT)
    print("%d tokens" % len(tokens))
    return tokens


for _ in range(1):

    test_rust()
    test_py()
