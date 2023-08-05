"""Standard library logger."""
from __future__ import annotations
from logging import Logger as StdlibLogger, getLogger
from typing import Any
from jhalog._base import LoggerBase
from jhalog._event import LogEvent


class Logger(LoggerBase):
    """Standard library logger."""

    __slots__ = ("_logger",)

    def __init__(
        self,
        logger: StdlibLogger | None = None,
        logger_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize logger.

        Args:
            logger: Standard library logger.
            logger_name: Standard library logger instance name.
                "logging.getLogger()" is used with this name to get the logger instance.
        """
        LoggerBase.__init__(self, **kwargs)
        self._logger = logger or getLogger(logger_name)

    def _emit(self, event: LogEvent) -> None:
        """Emit log event.

        Args:
            event: Log event.
        """
        self._emit_stdlib_logger(self._logger, event)
