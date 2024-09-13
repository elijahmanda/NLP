

from typing import (
    Tuple,
    List,
    Union,
    TypeVar,
    Optional,
    Literal,
)
import random
from random import randint, choice, random as _random_float
from num2words import num2words


_T = TypeVar("T")


class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(zip(self.keys(), self.values())))


def text_span_replace(text: str, replacement: str, span: Tuple[int, int]) -> str:
    """ Replace text[span[0] : span[1]] with `replacement` """
    left_chunk = text[0:span[0]]
    right_chunk = text[span[1]:]
    return left_chunk + replacement + right_chunk


def get_text_chunks(text: str, span: Tuple[int, int]) -> Tuple[str, str, str]:
    left_chunk = text[0:span[0]]
    right_chunk = text[span[1]:]
    middle_chunk = text[span[0]:span[1]]
    return left_chunk, middle_chunk, right_chunk


def pair(tokens: List[_T], *, holder: Optional[_T] = None) -> List[Tuple[_T, _T]]:
    """ When the token length is not an even number holder is used to make the length even by appending it. """
    tk_len = len(tokens)
    if tk_len == 1:
        return [(tokens[0], holder)]
    if tk_len % 2:
        tokens.append(holder)
        tk_len += 1
    new_tokens = []
    n = 0
    while n <= tk_len-1:
        new_tokens.append((tokens[n], tokens[n+1]))
        n += 2
    return new_tokens


def gen_nums(
    n: int,  # how many numbers
    *,
    num_range: int = (int(1e2), int(1e9)),
    num_points: int = 0,
    negative: bool = False,
    negative_name: str = "negative",
    point_name: str = "point",
) -> List[str]:
    nums = []
    for _ in range(n):
        num = random.randint(*num_range)
        points = "".join([str(randint(0, 9)) for _ in range(num_points)])
        if points:
            num = str(num) + "." + points
            num = float(num)
        word = num2words(num).replace("point", point_name)
        nums.append(word.split())
    negs = getattr(Language.get_data(), "NEGATIVES", [])
    if negative:
        for i, num in enumerate(nums):
            if num[0] != negative_name:
                if num[0] in negs:
                    nums[i][0] = negative_name
                else:
                    nums[i].insert(0, negative_name)

    return [" ".join(n) for n in nums]


def random_round(num: float, *, lower: int = 0, upper: int = 7) -> float:
    """
    Round off a number to a
    random number of decimal 
    places.
    """
    rd = randint(lower, upper)
    return round(num, rd)


def gen_exp_numbers(n: int, n_range: Tuple[int, int] = (-1000, 1000), exp_range: Tuple[int, int] = (1, 99)) -> List[str]:
    """ Generate exponential numbers"""
    letters = "eE"
    nums = []
    for _ in range(n):
        nums.append(
            str(
                random_round(
                    _random_float()*randint(*n_range))
            ) +
            choice(letters) +
            gen_sign() +
            str(randint(*exp_range))
        )
    return nums


def gen_ordinals(n: int, n_range: Tuple[int, int] = (1, 10000)) -> List[str]:
    rt = []
    end_map = {"1": "st", "2": "nd", "3": "rd"}
    for _ in range(n):
        num = str(randint(*n_range))
        end = num[-1]
        try:
            end_2 = num[-2]
        except IndexError:
            end_2 = None
        if end_2 == "1":
            suffix = "th"
        else:
            suffix = end_map.get(end)
            suffix = "th" if not suffix else suffix
        # print("utils:102:_gen_ordinals:->suffix:", suffix)
        # suffix = suffix if _random_float()>0.5 else suffix.upper()
        rt.append(num+suffix)
        # print("utils:102:_gen_ordinals:->num+suffix:", num+suffix)
    return rt


def gen_sign() -> Optional[Literal["+", "-"]]:
    signs = "+- "
    return choice(signs).strip()


def count_spaces(text: str) -> Tuple[int, int]:
    """
    Count the number of spaces
    at the left and right of a string.
    """
    left = right = 0
    for i in text:
        if i != " ":
            break
        left += 1
    for i in text[::-1]:
        if i != " ":
            break
        right += 1
    return (left, right)
