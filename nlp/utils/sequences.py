from typing import (
    List,
    Tuple,
    Any,
    TypeVar,
    Optional,
    Sequence,
)
import itertools


T = TypeVar("T")


def pair(tokens: List[T], *, holder: Optional[T] = None) -> List[Tuple[T, T]]:
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


def missing_indexes(indexes: Sequence[Tuple[int, int]], total: int) -> List[Tuple[int, int]]:
    if not any(indexes):
        return [(0, total)]
    missing = []
    if indexes[0][0] > 0:
        missing.append((0, indexes[0][0]))
    if indexes[-1][1] < total:
        missing.append((indexes[-1][1], total))
    for i, index in enumerate(indexes):
        if i < len(indexes) - 1:
            _, first_end = index
            next_start, _ = indexes[i + 1]
            if (next_start - first_end) > 0:
                missing.append((first_end, next_start))
    missing.sort()
    return missing


def pad_sequences(sequences: List[List[Any]], max_len: int, padding_value: Any = 0) -> List[List[Any]]:
    """Pads sequences with a padding value to a specified maximum length."""
    padded_sequences = []
    for sequence in sequences:
        if len(sequence) < max_len:
            padded_sequence = sequence + \
                [padding_value] * (max_len - len(sequence))
        else:
            padded_sequence = sequence[:max_len]
        padded_sequences.append(padded_sequence)
    return padded_sequences


def split_sequences(sequences: List[List[Any]], split_ratios: Tuple[float, float]) -> Tuple[List[List[Any]], List[List[Any]]]:
    """Splits sequences into two sets based on specified split ratios."""
    assert len(split_ratios) == 2, 'Split ratios must have length 2'
    assert sum(split_ratios) == 1, 'Split ratios must sum to 1'
    n = len(sequences)
    split_indices = (int(split_ratios[0] * n),
                     int((split_ratios[0] + split_ratios[1]) * n))
    train_sequences = sequences[:split_indices[0]]
    dev_sequences = sequences[split_indices[0]:split_indices[1]]
    test_sequences = sequences[split_indices[1]:]
    return train_sequences, dev_sequences, test_sequences


def shuffle_sequences(sequences: List[List[Any]]) -> List[List[Any]]:
    """Shuffles sequences randomly."""
    import random
    random.shuffle(sequences)
    return sequences


def flatten_sequences(sequences: List[List[Any]]) -> List[Any]:
    """Flattens a list of sequences into a single list."""
    return [item for sequence in sequences for item in sequence]


def count_tokens(sequences: List[List[Any]]) -> int:
    """Counts the total number of tokens in a list of sequences."""
    return sum(len(sequence) for sequence in sequences)


def _map_list(func, container):
    return list(map(func, container))


class AllEqual:

    def __init__(self, values: Sequence[T]):
        self._values = tuple(values)

    def __eq__(self, other: T) -> bool:
        return other in self

    def __hash__(self):
        return hash(self._values)

    def __contains__(self, value: Any):
        return value in self._values


def combinations(iterable, min_n):
    for i in range(len(iterable)):
        combs = itertools.combinations(iterable, i+min_n)
        for comb in combs:
            yield list(comb)


def reverse_dict(d):
    t = d.copy()
    d = dict(zip(t.values(), t.keys()))
    del t
    return d
