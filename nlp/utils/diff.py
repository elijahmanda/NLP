from difflib import SequenceMatcher
from pprint import pprint
from typing import List, Tuple

ch1 = """Today, a geentityation raised in the shadows of the Cold
     War assumes new responsibilities in a world warmed by the sunshine of
     freedom"""

ch2 = """Today, a geentityation raised in the shadows of the Cold
     War assumes responsibilities in a world warmed by the sunshine of
     spam and freedom"""


def text_diff(a: str, b: str):
    s = SequenceMatcher(None, a, b)
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        yield tag, (i1, i2), (j1, j2), a[i1:i2], b[j1:j2]


def get_missing_indices(indices: List[Tuple[int, int]], total_length: int) -> List[Tuple[int, Tuple[int, int]]]:
    if not any(indices):
        return []
    missing = []
    if indices[0][0] > 0:
        missing.append((0, (0, indices[0][0])))
    if len(indices) > 1:
        if indices[-1][1] < total_length:
            missing.append((-1, (indices[-1][1], total_length)))
    i = 1
    while i < len(indices) - 1:
        s, e = indices[i-1][1], indices[i][0]
        if s != e:
            missing.append((i, (s, e)))
        i += 1

    return missing

# indices = [(3,8), (10, 12)]
# total_len = 20
# missing = get_missing_indices(indices, total_len)
# print(indices)
# print(missing)
# exit()

# text = "i met them on Jan. 12th, 2005. two days after 10/03/78 at 10:34pm and 10 AM"

# print(list(text_diff(ch1, ch2)))
