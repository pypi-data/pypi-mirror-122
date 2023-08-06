import re

_non_numeric = re.compile(r'[^\d]+')

__all__ = [
    "strip_non_numeric"
]


def strip_non_numeric(s: str) -> str:
    return _non_numeric.sub('', s)
