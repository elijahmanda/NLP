import sys
import importlib
from typing import Set, Optional, Type

from nlp.entity import EntityParser

__all__ = ["AVAILABLE_PARSERS", "load_parser"]

AVAILABLE_PARSERS: Set[str] = {
    "email",
    "ip",
    "number",
    # "gpe",
    "symbol",
    "currency",
    # "event",
    "uri",
}


def load_parser(name: str, /, **kwargs) -> Optional[EntityParser]:
    if name not in AVAILABLE_PARSERS:
        raise Exception("No parser with name %r" % name) from None
    module = importlib.import_module(f"nlp.parsers.{name}")
    parser_class = module.get_parser()
    parser = parser_class(**kwargs)
    return parser
