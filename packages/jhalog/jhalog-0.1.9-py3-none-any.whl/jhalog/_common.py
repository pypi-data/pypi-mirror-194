"""Common utilities."""
from typing import TypedDict
import jhalog  # noqa


class _Cache(TypedDict, total=False):
    """Cached values."""

    default_logger: "jhalog._base.LoggerBase"
    process_create_time: float
    boot_time: float


CACHE: _Cache = dict()


def process_create_time() -> float:
    """Get process creation time.

    Returns:
        Process creation time.
    """
    try:
        return CACHE["process_create_time"]
    except KeyError:
        from psutil import Process

        value = CACHE["process_create_time"] = Process().create_time()
        return value


def boot_time() -> float:
    """Get OS boot time.

    Returns:
        Process creation time.
    """
    try:
        return CACHE["boot_time"]
    except KeyError:
        from psutil import boot_time

        CACHE["boot_time"] = value = boot_time()
        return value
