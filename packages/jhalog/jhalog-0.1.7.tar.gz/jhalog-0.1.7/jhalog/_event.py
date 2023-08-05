"""The log event object."""
from __future__ import annotations
from contextvars import ContextVar
from datetime import datetime, timezone
from ipaddress import IPv4Address, IPv6Address
from time import perf_counter, time
from traceback import format_exception
from types import TracebackType
from typing import Any, Type, MutableMapping
from webuuid import Uuid
import jhalog._base  # noqa
from jhalog._common import boot_time, process_create_time, CACHE
from jhalog.exceptions import (
    LogEventNotFoundException,
    LogEventAlreadyEmittingException,
)
from jhalog.typing import HttpMethod, Fields, EventLevel


class LogEvent(MutableMapping[str, Any]):
    """Log Event."""

    __slots__ = ("_dict", "_logger", "_done", "_locked", "_start")

    #: Default JSON encoder, can be updated to support more classes
    JSON_ENCODERS = {datetime: lambda v: v.isoformat()}

    def __init__(
        self,
        logger: "jhalog._base.LoggerBase | None" = None,
        context: bool = True,
        **fields: Any,
    ) -> None:
        """Initialize log event.

        Args:
            logger: Logger to use to emit this log event.
            context: If True, set this log event as current context log event.
            **fields: Fields to add.
        """
        self._done = False
        self._locked = False
        try:
            self._logger = logger or CACHE["default_logger"]
        except KeyError:
            raise ValueError("A logger is required.") from None
        if context:
            context_log_event.set(self)
        self._dict: Fields = dict(
            type="access", level="info", date=datetime.now(timezone.utc)
        )
        self.set(**fields)

    def __enter__(self) -> "LogEvent":
        self._start = perf_counter()
        self._locked = True
        return self

    def __exit__(self, *_: Any) -> None:
        self.execution_time = perf_counter() - self._start
        self._locked = False
        self.emit()

    def __del__(self) -> None:
        self._locked = False
        self.emit()

    def __delitem__(self, field: str) -> None:
        try:
            self._dict.__delitem__(field)  # type: ignore
        except KeyError:
            return

    __delattr__ = __delitem__

    def __getitem__(self, field: str) -> Any:
        return self._dict.__getitem__(field)

    def __setitem__(self, field: str, value: Any) -> None:
        try:
            setattr(self, field, value)
        except AttributeError:
            self._set(field, value)

    def __iter__(self) -> Any:
        return self._dict.__iter__()

    def __len__(self) -> int:
        return self._dict.__len__()

    def __repr__(self) -> str:
        return f"LogEvent({self._dict})"

    def __str__(self) -> str:
        return self._dict.__str__()

    def __hash__(self) -> int:
        return self._dict.__hash__()

    def _set(self, field: str, value: Any) -> None:
        """Set value, if not None.

        Args:
            field: Field.
            value: Value.
        """
        if value is not None:
            self._dict[field] = value  # type: ignore

    def emit(self) -> None:
        """Emit log event."""
        if self._locked:
            raise LogEventAlreadyEmittingException("Event already processing.")
        elif not self._done:
            self._logger._emit_by_level(self)
            self._done = True

    def cancel(self) -> None:
        """If called, the log event will be cancelled and not emitted by the logger."""
        self._done = True

    @property
    def done(self) -> bool:
        """Log event state.

        Returns:
            True if log event has been emitted or cancelled.
        """
        return self._done

    @property
    def dict(self) -> Fields:
        """Log event dictionary.

        Returns:
            Log event dictionary.
        """
        return self._dict

    @property
    def logger(self) -> "jhalog._base.LoggerBase":
        """Get Logger attached to this event."""
        return self._logger

    @staticmethod
    def from_context() -> "LogEvent":
        """Get log event from context.

        Returns:
            Context log event.

        Raises:
            LogEventNotFoundException: No context log event.
        """
        try:
            return context_log_event.get()
        except LookupError:
            raise LogEventNotFoundException(
                "No log event in the current context."
            ) from None

    def get(self, field: str, default: Any = None) -> Any:
        """Get a field value.

        Args:
            field: Field to get.
            default: If specified return this value if the value is missing.
                If not specified, returns None.
        """
        return self._dict.get(field, default)

    @staticmethod
    def get_from_context(field: str, default: Any = None) -> Any:
        """Get a field value from the context log event if any.

        Args:
            field: Field to get.
            default: If specified return this value if the log event does not exist
                of the value is missing in the context. If not specified, returns None.
        """
        try:
            return context_log_event.get().get(field, default)
        except LookupError:
            return default

    def set(self, **fields: Any) -> None:
        """Set field(s) to the log event.

        None values are ignored when using this method.

        Args:
            fields: Fields to set.
        """
        for field, value in fields.items():
            self[field] = value

    @staticmethod
    def set_to_context(**fields: Any) -> None:
        """Set field(s) to the context log event if any.

        Do nothing if there is no context log event.

        Args:
            fields: Fields to set.
        """
        try:
            event = context_log_event.get()
        except LookupError:
            return
        event.set(**fields)

    @property
    def client_id(self) -> Any:
        """Client ID.

        Returns:
            Value.
        """
        return self._dict["client_id"]

    @client_id.setter
    def client_id(self, value: Any | None) -> None:
        """Set client ID.

        Args:
            value: Value.
        """
        self._set("client_id", value)

    @property
    def client_ip(self) -> str:
        """Client IP address.

        Returns:
            Value.
        """
        return self._dict["client_ip"]

    @client_ip.setter
    def client_ip(self, value: IPv4Address | IPv6Address | str | None) -> None:
        """Set client IP.

        Check if storing IP address in log is allowed first.

        Args:
            value: Value.
        """
        if self._logger.ip_addresses_allowed and value:
            self._set("client_ip", str(value))

    @property
    def client_jti(self) -> str:
        """Client JTI (JSON Web Token ID).

        Returns:
            Value.
        """
        return self._dict["client_jti"]

    @client_jti.setter
    def client_jti(self, value: str | None) -> None:
        """Set client JTI.

        Args:
            value: Value.
        """
        self._set("client_jti", value)

    @property
    def client_type(self) -> str:
        """Client type.

        Returns:
            Value.
        """
        return self._dict["client_type"]

    @client_type.setter
    def client_type(self, value: str | None) -> None:
        """Set client type.

        Args:
            value: Value.
        """
        self._set("client_type", value)

    @property
    def client_user_agent(self) -> str:
        """Client user agent ("User-Agent" HTTP header).

        Returns:
            Value.
        """
        return self._dict["client_user_agent"]

    @client_user_agent.setter
    def client_user_agent(self, value: str | None) -> None:
        """Set client user agent.

        Args:
            value: Value.
        """
        self._set("client_user_agent", value)

    @property
    def created(self) -> list[Any]:
        """Identifiers of resources created during the event.

        For instance, should contain returned IDs of HTTP POST with 201 status code.

        The list is automatically initialized on first call.

        Returns:
            Value.
        """
        try:
            return self._dict["created"]
        except KeyError:
            self._dict["created"] = list()
            return self._dict["created"]

    @created.setter
    def created(self, value: list[Any]) -> None:
        """Set created.

        Args:
            value: Value.
        """
        self._set("created", value)

    @property
    def date(self) -> Any:
        """Event date.

        Timezone is UTC.

        Returns:
            Value.
        """
        return self._dict["date"]

    @date.setter
    def date(self, value: datetime) -> None:
        """Set date.

        Args:
            value: Value.
        """
        self._set("date", value)

    @property
    def error_detail(self) -> Any:
        """Internal error detail.

        Returns:
            Value.
        """
        return self._dict["error_detail"]

    @error_detail.setter
    def error_detail(self, value: Any | None) -> None:
        """Set error detail.

        Args:
            value: Value.
        """
        self._set("error_detail", value)

    def error_detail_from_exception(
        self,
        exc_value: BaseException,
        exc_type: Type[BaseException] | None = None,
        exc_traceback: TracebackType | None = None,
    ) -> None:
        """Set "level" and "error_detail" fields from an exception.

        The "level" field is set to "critical".

        The "error_detail" field is set to the exception traceback.

        Args:
            exc_value: Exception value.
            exc_type: Exception type.
            exc_traceback: Exception traceback.
        """
        self._dict["level"] = "critical"
        self._dict["error_detail"] = "".join(
            format_exception(
                exc_type or type(exc_value),
                exc_value,
                exc_traceback or exc_value.__traceback__,
            )
        )

    @property
    def execution_time(self) -> float:
        """Event execution time in seconds.

        Returns:
            Value.
        """
        return self._dict["execution_time"]

    @execution_time.setter
    def execution_time(self, value: float | int) -> None:
        """Set execution time.

        Returns:
            Value (seconds).
        """
        self._dict["execution_time"] = round(value, 6)

    @property
    def level(self) -> EventLevel:
        """Level.

        Returns:
            Value.
        """
        return self._dict["level"]

    @level.setter
    def level(self, value: EventLevel) -> None:
        """Set level.

        Args:
            value: Value.
        """
        self._set("level", value)

    @property
    def method(self) -> HttpMethod:
        """HTTP method.

        Returns:
            Value.
        """
        return self._dict["method"]

    @method.setter
    def method(self, value: HttpMethod) -> None:
        """Set method.

        Returns:
            Value.
        """
        self._set("method", value)

    @property
    def os_uptime(self) -> float:
        """OS uptime in seconds.

        Returns:
            Value.
        """
        try:
            return self._dict["os_uptime"]
        except KeyError:
            return self.os_uptime_calculate()

    @os_uptime.setter
    def os_uptime(self, value: float | int) -> None:
        """Set OS uptime.

        Returns:
            Value (seconds).
        """
        self._dict["os_uptime"] = round(value, 6)

    def os_uptime_calculate(self) -> float:
        """Calculate OS uptime field value.

        Returns:
            Value.
        """
        self.os_uptime = process_create_time() - boot_time()
        return self._dict["os_uptime"]

    @property
    def path(self) -> str:
        """HTTP path.

        Returns:
            Value.
        """
        return self._dict["path"]

    @path.setter
    def path(self, value: str) -> None:
        """Set path.

        Returns:
            Value.
        """
        if value in self._logger.ignored_path:
            self.cancel()
        self._set("path", value)

    @property
    def request_id(self) -> str:
        """Request ID ("X-request-ID" HTTP header).

        If not set previously, set it to a new random value and return it.

        Returns:
            Value.
        """
        try:
            return self._dict["request_id"]
        except KeyError:
            self._dict["request_id"] = Uuid().base64url()
            return self._dict["request_id"]

    @request_id.setter
    def request_id(self, value: str | None) -> None:
        """Set request ID.

        Args:
            value: Value.
        """
        self._set("request_id", value)

    @property
    def server_id(self) -> str:
        """Server ID.

        Returns:
            Value.
        """
        return self._dict["server_id"]

    @server_id.setter
    def server_id(self, value: str) -> None:
        """Set server ID.

        Args:
            value: Value.
        """
        self._set("server_id", value)

    @property
    def server_version(self) -> str:
        """Server version.

        Returns:
            Value.
        """
        return self._dict["server_version"]

    @server_version.setter
    def server_version(self, value: str) -> None:
        """Set server version.

        Args:
            value: Value.
        """
        self._set("server_version", value)

    @property
    def server_uptime(self) -> float:
        """Server uptime in seconds.

        Returns:
            Value.
        """
        try:
            return self._dict["server_uptime"]
        except KeyError:
            return self.server_uptime_calculate()

    @server_uptime.setter
    def server_uptime(self, value: float | int) -> None:
        """Set server uptime.

        Returns:
            Value (seconds).
        """
        self._dict["server_uptime"] = round(value, 6)

    def server_uptime_calculate(self) -> float:
        """Calculate server uptime field value.

        Returns:
            Value.
        """
        self.server_uptime = time() - process_create_time()
        return self._dict["server_uptime"]

    @property
    def status_code(self) -> int:
        """HTTP status code.

        Returns:
            Value.
        """
        return self._dict["status_code"]

    @status_code.setter
    def status_code(self, value: int) -> None:
        """Set status code.

        Also set the "level" field based on the status codes: Set to "warning" for
        4XX codes and "error" for 5XX codes.

        Args:
            value: Value.
        """
        self._dict["status_code"] = value
        if 100 <= value < 400:
            try:
                # Remove caught exception messages if any
                del self._dict["error_detail"]
            except KeyError:
                pass
        elif 400 <= value < 500:
            self._dict["level"] = (
                "warning" if self._dict["level"] != "critical" else "critical"
            )
        elif 500 <= value < 600:
            self._dict["level"] = (
                "error" if self._dict["level"] != "critical" else "critical"
            )
        else:
            raise ValueError(f"Invalid HTTP status code: {value}")

    def status_code_from_exception(self, exception: BaseException) -> tuple[int, str]:
        """Set "status_code", "level" and "error_detail" fields from an exception.

        The "status_code" is selected based on the exception and is generally
        a 5XX code (500 if nothing more specific found).

        The "level" field is set to "critical".

        The "error_detail" field is set to the exception traceback.

        Also return the selected status code and the associated message.

        Args:
            exception: Exception.

        Returns:
            Status code, message
        """
        self.error_detail_from_exception(exception)
        for func in self._logger._exception_to_status_code:
            status = func(exception)
            if status:
                break
        else:
            status = 500, "Internal Server Error"
        self._dict["status_code"] = status[0]
        return status

    @property
    def type(self) -> str:
        """Event type.

        Returns:
            Value.
        """
        return self._dict["type"]

    @type.setter
    def type(self, value: str) -> None:
        """Event type.

        Args:
            value: Value.
        """
        self._set("type", value)


context_log_event: ContextVar[LogEvent] = ContextVar("context_log_event")
