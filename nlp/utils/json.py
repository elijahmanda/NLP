from typing import Sequence


def filter_comments(data: Sequence[str]) -> str:
    stripped = ""
    for datum in data:
        if not datum.strip().strip().startswith(("//", "#")):
            stripped += datum
    return stripped
