from typing import Tuple
import string

from nlp.constants import DEFAULT_ENCODING

PUNCTUATION = set(string.punctuation)


def encode(text: str) -> bytes:
    return text.encode(DEFAULT_ENCODING)


def decode(byte_string: bytes) -> str:
    return byte_string.decode(DEFAULT_ENCODING)


def text_span_replace(text, replacement, start, end):
    """ Replace text[span[0] : span[1]] with `replacement` """
    tmp = bytearray(encode(text))
    tmp[start: end] = encode(replacement)
    tmp = decode(tmp)
    return tmp


def count_spaces(text: str) -> Tuple[int, int]:
    text_len = len(text)
    left = text_len - len(text.lstrip())
    right = text_len - len(text.rstrip())
    return (left, right)


def get_text_chunks(text: str, span: Tuple[int, int]) -> Tuple[str, str, str]:
    left_chunk = text[0:span[0]]
    right_chunk = text[span[1]:]
    middle_chunk = text[span[0]:span[1]]
    return left_chunk, middle_chunk, right_chunk


def has_punct(text: str) -> bool:
    return bool(set(text) & PUNCTUATION)


def has_space(text: str) -> bool:
    return " " in text


def remove_spaces(text: str) -> str:
    return "".join(text.split())


def remove_multiple_spaces(text):
    return " ".join(text.split())


class CaseLessString(str):

    def __eq__(self, other):
        if not isinstance(other, str):
            return False
        return self.lower() == other.lower()

    def __hash__(self):
        return hash(str(self))
