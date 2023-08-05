"""Cloudwatch logs common."""
from typing import TypedDict
from jhalog._event import LogEvent
from jhalog.exception_handlers.botocore import get_status_from_botocore_error


class CloudwatchLogEvent(TypedDict):
    """Cloudwatch log event."""

    message: str
    timestamp: int


class CloudwatchLogsBase:
    """Cloudwatch Logger."""

    # Cloudwatch Logs put_log_events limits
    _BATCH_SIZE_LIMIT = 1048576  # bytes
    _BATCH_COUNT_LIMIT = 10000

    # Retries count in case of Cloudwatch unavailability
    # Using a large default value to maximise chances logs are flushed.
    _RETRIES_MAX_ATTEMPTS = 100

    __slots__ = ("_client", "_client_kwargs", "_json_dumps")

    def __init__(self, log_group_name: str) -> None:
        """Initialize logger.

        Args:
            log_group_name: Cloudwatch Logs log group where to create the log stream
                where log event will be put. The log group must exist.
        """
        self._client_kwargs = dict(logGroupName=log_group_name)
        self.add_exception_handler(get_status_from_botocore_error)  # type: ignore

    def _format_log_event(self, event: LogEvent) -> CloudwatchLogEvent:
        """Format log event.

        Args:
            event: Log event.

        Returns:
             Cloudwatch formatted Log event.
        """
        timestamp = int(event.dict.pop("date").timestamp() * 1000)
        message: str = self._json_dumps(event)  # type: ignore
        return {"timestamp": timestamp, "message": message}

    @staticmethod
    def _get_log_event_size(log_event: CloudwatchLogEvent) -> int:
        """Get a Cloudwatch log event size.

        Args:
            log_event: Cloudwatch formatted log event

        Returns:
            Event size.
        """
        return len(log_event["message"].encode()) + 26
