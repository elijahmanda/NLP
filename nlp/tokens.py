# coding: utf-8
# cython: embedsignature=True
# cython: language_level=3

import copy
import json
import yaml
from enum import Enum
from dataclasses import (
    dataclass,
    field,
)


def _json_default(obj):
    try:
        return obj.to_dict()
    except AttributeError:
        pass
    return obj


DUMPERS = {
    "json": lambda obj, **kwargs: json.dumps(obj, ensure_ascii=False, indent=2, default=_json_default, **kwargs),
    "yaml": lambda obj, **kwargs: yaml.dump(obj, indent=2),
}


class DumpFormat(Enum):
    JSON = "json"
    YAML = "yaml"


DEFAULT_DUMPER = DumpFormat.JSON


class Token:
    """Represents a token in a text."""

    def __init__(
        self,
        text: str,
        entity: str = None,
        span: tuple[int, int] = (None, None),
        lineno: int = None,
        metadata: dict = None,
    ):
        self.text = text
        self.entity = entity
        self.span = span
        self.lineno = lineno
        self.metadata = metadata or {}

    def __hash__(self):
        item = (self.text, self.span, self.entity)
        return hash(item)

    def to_dict(self):
        return {
            "text": self.text,
            "span": self.span,
            "lineno": self.lineno,
            "entity": self.entity,
            "metadata": self.metadata,
        }

    def __repr__(self):
        except_ = ["text", "metadata"]
        msg = f"{self.__class__.__name__}(text={self.text!r}"
        for key, value in self.to_dict().items():
            if value is not None and key not in except_:
                if isinstance(value, str):
                    msg += f", {key}={value!r}"
                else:
                    msg += f", {key}={value}"
        msg += ")"
        return msg

    def __str__(self):
        return self.text

    def dumps(self, dumper: DumpFormat = None):
        dumper = dumper or DEFAULT_DUMPER
        data = self.to_dict() or {}
        if isinstance(
                ((data.get("metadata") or {}).get("value")), complex):
            data["metadata"]["value"] = str(data["metadata"]["value"])
        dumped = DUMPERS[dumper.value](data)
        return dumped
