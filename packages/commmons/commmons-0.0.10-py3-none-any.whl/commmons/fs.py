import os
from pathlib import Path

__all__ = [
    "get_filesize_in_bytes",
    "touch"
]


def get_filesize_in_bytes(path: str):
    if os.path.isdir(path):
        raise ValueError('folders are not supported')

    s = os.stat(path)
    return s.st_size


def touch(path: str, is_directory=False):
    if os.path.exists(path):
        return

    os.makedirs(Path(path).parent, exist_ok=True)
    open(path, "a").close()


def touch_directory(path: str):
    touch(path, is_directory=True)
