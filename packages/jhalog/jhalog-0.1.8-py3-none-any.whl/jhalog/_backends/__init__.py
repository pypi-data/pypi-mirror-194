"""Logging backends."""
from importlib import import_module
from typing import Any
from jhalog._base import LoggerCoreBase


class Logger(LoggerCoreBase):
    """Logger."""

    def __new__(cls, backend: str = "logging", *args: Any, **kwargs: Any) -> "Logger":
        """Logger factory."""
        element = f"{__name__}.{backend}"
        try:
            module = import_module(element)
        except ImportError:
            from importlib.util import find_spec

            if find_spec(element) is not None:  # pragma: no cover
                raise
            raise NotImplementedError(f"Unsupported backend: {backend}")
        return getattr(module, "Logger")(  # type: ignore
            backend=backend, *args, **kwargs
        )

    def __enter__(self) -> "Logger":
        return self  # pragma: no cover

    def __exit__(self, *_: Any) -> None:
        pass  # pragma: no cover

    async def __aenter__(self) -> "Logger":
        return self  # pragma: no cover

    async def __aexit__(self, *_: Any) -> None:
        pass  # pragma: no cover


class AsyncLogger(LoggerCoreBase):
    """Async logger."""

    def __new__(
        cls, backend: str = "logging", *args: Any, **kwargs: Any
    ) -> "AsyncLogger":
        """Async Logger factory."""
        element = f"{__name__}.{backend}_async"
        try:
            module = import_module(element)
        except ImportError:
            from importlib.util import find_spec

            if find_spec(element) is not None:  # pragma: no cover
                raise
            return Logger(backend=backend, *args, **kwargs)  # type: ignore
        return getattr(module, "Logger")(  # type: ignore
            backend=backend, *args, **kwargs
        )

    async def __aenter__(self) -> "AsyncLogger":
        return self  # pragma: no cover

    async def __aexit__(self, *_: Any) -> None:
        pass  # pragma: no cover
