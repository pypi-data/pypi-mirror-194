from typing import Callable

from .concatenate import concatenate
from .env import env

Merger = Callable[[bytes, bytes], bytes]


def get(source_type: str, dest_type: str) -> Merger:
    """
    Return the correct file merger
    """

    if source_type == ".env" and dest_type == ".env":
        return env
    else:
        return concatenate
