from __future__ import annotations

import typing as t
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Config:
    language: str = "en"
    signs_allowed: bool = False
    parse_complex: bool = False
    bounded_numbers: bool = False
    use_decimal: bool = False
    round_to: int | None = None
    mixed_nums: bool = True
    merge: bool = True
    merge_multiples: bool = True
    merge_implied: bool = False
    merge_points: bool = False
    merge_informals: bool = True
    exclude_separators: t.Tuple[t.Literal[",", "'", "_"]] | None = None
    exclude_suffixes: t.Tuple[str] | None = ("m", "y")
    # Second excluded because its ambiguous to second for time and second for ordinals
    exclude_ordinal_ones: t.Tuple[str] | None = ("second",)
