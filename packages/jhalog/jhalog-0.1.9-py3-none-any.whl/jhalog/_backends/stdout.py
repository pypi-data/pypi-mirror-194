"""STDOUT logger."""
from jhalog._base import LoggerBase
from jhalog._event import LogEvent


class Logger(LoggerBase):
    """STDOUT logger."""

    def _emit(self, event: LogEvent) -> None:
        """Emit log event.

        Args:
            event: Log event.
        """
        print(self._json_dumps(event))
