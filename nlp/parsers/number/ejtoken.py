import re
from typing import List


class Tokenizer:

    # starting quotes
    STARTING_QUOTES = [
        (re.compile(r"^[\"']"), r"``"),
        (re.compile(r"(``)"), r" \1 "),
        (re.compile(r"([ \(\[{<])(\"|\'{2})"), r"\1 `` "),
    ]

    # punctuation
    PUNCTUATION = [
        (re.compile(r"([,'])([^\d])"), r"  \1   \2"),
        (re.compile(r"([:,])$"), r" \1 "),
        (re.compile(r"[;@#%&/:?!]"), r"   \g<0>   "),
    ]

    # Pads parentheses
    PARENS_BRACKETS = (re.compile(r"[\]\[\(\)\{\}\<\>]"), r"   \g<0>   ")

    DOUBLE_DASHES = (re.compile(r"--"), r"   --   ")

    # ending quotes
    ENDING_QUOTES = [
        (re.compile(r"([\D])([\"'])(\d)"), r"  \1   \2   \3  "),
        (re.compile(r"([\"'])([\D])"), r"  \1   \2  "),
        (re.compile(r"([\D])([\"'])"), r"  \1   \2  "),
    ]

    def tokenize(
        self, text: str
    ) -> List[str]:
        text = f" {text} "
        for regexp, substitution in self.STARTING_QUOTES:
            text = regexp.sub(substitution, text)
            # print("\nText:", text, "\nRegex:", regexp)

        for regexp, substitution in self.PUNCTUATION:
            text = regexp.sub(substitution, text)
            # print("\nText:", text, "\nRegex:", regexp)

        # Handles parentheses.
        regexp, substitution = self.PARENS_BRACKETS
        text = regexp.sub(substitution, text)
        # print("\nText:", text, "\nRegex:", regexp)

        # Handles double dash.
        regexp, substitution = self.DOUBLE_DASHES
        text = regexp.sub(substitution, text)
        # print("\nText:", text, "\nRegex:", regexp)

        # add extra space to make things easier
        text = " " + text + " "

        for regexp, substitution in self.ENDING_QUOTES:
            text = regexp.sub(substitution, text)
            # print("\nText:", text, "\nRegex:", regexp)

        return text.split()

    def __call__(self, text):
        return self.tokenize(text)


tokenizer = Tokenizer()


def tokenize(text: str) -> list[str]:
    return tokenizer.tokenize(text)


if __name__ == "__main__":
    txt = """
    1 -89 +799 588
    2.5 .577 1.2e2 23E3 -208.89 +13.7
    -2.7e2 +199.123E90 +5e-12 -.5
    -0.244e+19
    2,000 12,999 123,689 2,078,689
    12,089,688 1,230.0971 799,089.13
    124,799,799,588.8981349901
    2,008e10 -12,899 +77,089 9,000.7
    -134,799 -6,799.999 +13,689E-12
    +799,799e+1 -67,799.968e-123
    +78,000E10 -123,147E2
    2'000 12'999 123'689 2'078'689
    12'089'688 1'230.0971 799'089.13
    124'799'799'588.8981349901
    2'008e10 -12'899 +77'089 9'000.7
    -134'799 -6'799.999 +13'689E-12
    +799'799e+1 -67'799.968e-123
    +144'478E10 -133'899E2
    1k -89M +799B 588m
    2.5c .577G 1.2e2T 23E3Z -208.89y
    """
    from nlp.utils.timer import timer
    expected = len(timer()(txt.split)())
    print("Expected length:", expected)

    for _ in range(5):
        toktok = len(timer()(tokenize)(txt))
        print("Toktok Length:", toktok)

    assert expected == toktok
