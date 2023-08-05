"""Logger base classes."""
from __future__ import annotations
from socket import gethostname
from os import getpid
from types import TracebackType
import sys
from abc import ABC, abstractmethod
from json import dumps
from logging import Logger as StdlibLogger, getLevelName
from typing import Callable, Any, Iterable, Type
from jhalog.exceptions import LoggerNotReadyException
from jhalog._event import LogEvent
from jhalog._common import CACHE


class LoggerCoreBase(ABC):
    """Logger core base.

    Used by abstract base classes and factories.
    """

    __slots__ = (
        "_backend",
        "_default_fields",
        "_json_dumps_func",
        "_sys_excepthook",
        "_exception_to_status_code",
        "_level",
        "_stdlib_logger",
        "_allow_ip_addresses",
        "_ignore_paths",
        "_calculate_uptime",
        "_server_version",
    )

    def __init__(
        self,
        backend: str = "logging",
        json_dumps: Callable[..., str] = dumps,
        default_fields: dict[str, Any] | None = None,
        exception_hook: bool = False,
        level: str = "info",
        logger: StdlibLogger | None = None,
        ip_addresses_allowed: bool = False,
        ignored_paths: Iterable[str] | None = None,
        calculate_uptime: bool = True,
        server_version: str | None = None,
    ) -> None:
        """Initialize logger.

        Args:
            backend: Logging backend to use.
            json_dumps: JSON serialization method to use in place of "json.dumps".
            default_fields: Default fields to add to all logs events on creation.
            exception_hook: Register an exception hook (With "sys.excepthook") to
                ensure all unhandled exceptions are logged.
            level: Minimal "event" of log events. Log events with levels below this
                value are not emitted.
            logger: A standard library logger were additionally emit log events.
            ip_addresses_allowed: If True, IP addresses are allowed in logs events.
                Useful for privacy and compliance.
            ignored_paths: Logs events with the "path" field in this list are not
                emitted.
            calculate_uptime: Automatically calculate "os_uptime" and "server_uptime"
                values on "startup" and "shutdown" log events.
            server_version: Server version to add to the "server_version" field on
                "startup" log events.
        """
        self._backend = backend
        self._json_dumps_func = json_dumps
        self._exception_to_status_code = [self._get_status_code_for_timeout]
        self._level = getLevelName(level.upper())
        self._stdlib_logger = logger
        self._calculate_uptime = calculate_uptime
        self._server_version = server_version

        # Event config
        self._ip_addresses_allowed = ip_addresses_allowed
        self._ignored_paths = set(ignored_paths) if ignored_paths else set()

        self._default_fields = default_fields or dict()
        self._set_default_server_field()

        if exception_hook:
            self._sys_excepthook = sys.excepthook
            sys.excepthook = self._emit_excepthook_event

    def add_exception_handler(
        self, handler: Callable[..., tuple[int, str] | None]
    ) -> None:
        """Add an Exception handler to convert exception to status code.

        Args:
            handler: Exception handler.

        Returns:
            Exception handler.
        """
        self._exception_to_status_code.append(handler)

    @property
    def ignored_path(self) -> set[str]:
        """Paths that are ignored in logs.

        Returns:
            Paths.
        """
        return self._ignored_paths

    @property
    def ip_addresses_allowed(self) -> bool:
        """If True, allow IP addresses in logs ("client_ip" field).

        Disabling IP addresses if useful for privacy and compliance.

        Returns:
            If True, allow IP addresses.
        """
        return self._ip_addresses_allowed

    @property
    def backend(self) -> str:
        """Backend.

        Returns:
            Backend name.
        """
        return self._backend

    def create_event(self, context: bool = True, **fields: Any) -> LogEvent:
        """Create a new log event.

        Args:
            context: If True, set as context log event.
            fields: Other initial fields to add.

        Returns:
            Log event.
        """
        self._check_ready()
        kwargs = self._default_fields.copy()
        kwargs.update(fields)
        return LogEvent(self, context=context, **kwargs)  # type: ignore

    def _check_ready(self) -> None:
        """Check if the logger is ready to emit events.

        Raises:
            LoggerNotReadyException if not ready.
        """

    def emit_startup_completed_event(self, **fields: Any) -> None:
        """Emit a log event indicating startup is completed.

        Args:
            fields: Extra fields.
        """
        event = self.create_event(context=False, type="startup", **fields)
        event.set(server_version=self._server_version)
        if self._calculate_uptime:
            event.os_uptime_calculate()
            event.server_uptime_calculate()
        event.emit()

    def emit_shutdown_completed_event(self, **fields: Any) -> None:
        """Emit a log event indicating shutdown is completed.

        Args:
            fields: Extra fields.
        """
        event = self.create_event(context=False, type="shutdown", **fields)
        if self._calculate_uptime:
            event.server_uptime_calculate()
        event.emit()

    def _emit_stdlib_logger(self, logger: StdlibLogger | None, event: LogEvent) -> None:
        """Emit og event to a standard library logger.

        Args:
            logger: Standard library logger.
            event: Log event.
        """
        if logger is not None:
            getattr(logger, event.level)(self._json_dumps(event))

    def _emit_excepthook_event(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType | None,
    ) -> None:
        """Log uncaught exceptions.

        Args:
            exc_type: Exception type.
            exc_value: Exception value.
            exc_traceback: Exception traceback.
        """
        try:
            event = self.create_event(context=False, type="uncaught_exception")
            event.error_detail_from_exception(
                exc_type=exc_type, exc_value=exc_value, exc_traceback=exc_traceback
            )
            event.emit()
        finally:
            self._sys_excepthook(exc_type, exc_value, exc_traceback)

    def _json_dumps(self, event: LogEvent) -> str:
        """Dumps log event to JSON.

        Args:
            event: Event.

        Returns:
            JSON serialized event.
        """
        return self._json_dumps_func(event.dict, default=self._json_default)

    @staticmethod
    def _json_default(obj: Any) -> Any:
        """Default serializer.

        Args:
            obj: Object to serialize.
        """
        for obj_type, func in LogEvent.JSON_ENCODERS.items():
            if isinstance(obj, obj_type):
                return func(obj)  # type: ignore
        raise TypeError

    @staticmethod
    def _get_status_code_for_timeout(
        exception: BaseException,
    ) -> tuple[int, str] | None:
        """Return 504 "Gateway Timeout" on TimeoutError exceptions.

        Args:
            exception: Exception.

        Returns:
            Status code, message
        """
        if isinstance(exception, TimeoutError):
            return 504, "Gateway Timeout"
        return None

    def _set_default_server_field(self, server_id: str | None = None) -> None:
        """Set the default server field.

        Args:
            server_id: Server ID.
        """
        self._default_fields["server_id"] = (
            f"{server_id or self._get_server_id()}-{getpid()}"
        )

    @staticmethod
    def _get_server_id() -> str:
        """Get server identifier.

        The value should uniquely identify the server.

        Returns:
            Server identifier.
        """
        return gethostname()


class LoggerBase(LoggerCoreBase):
    """Logger abstract base class.

    The main abstract base class.
    """

    def __init__(self, default_logger: bool = True, **kwargs: Any) -> None:
        """Initialize logger.

        Args:
            default_logger: If set to True, this logger is used when creating a
                jhalog.LogEvent instance directly without specifying a logger.
        """
        LoggerCoreBase.__init__(self, **kwargs)
        if default_logger:
            CACHE["default_logger"] = self

    def __enter__(self) -> "LoggerBase":
        return self

    def __exit__(self, *_: Any) -> None:
        self.emit_shutdown_completed_event()

    async def __aenter__(self) -> "LoggerBase":
        return self.__enter__()

    async def __aexit__(self, *_: Any) -> None:
        self.__exit__()

    @abstractmethod
    def _emit(self, event: LogEvent) -> None:
        """Emit log event.

        Args:
            event: Log event.
        """

    def _emit_by_level(self, event: LogEvent) -> None:
        """Emit log event if match the current log filter.

        Should be called from LogEvent object only.

        Args:
            event: Log event.
        """
        if not event.done:
            if getLevelName(event.level.upper()) >= self._level:
                self._emit(event)
            self._emit_stdlib_logger(self._stdlib_logger, event)


class BackgroundLoggerBase(LoggerBase):
    """Background logger abstract base class.

    The abstract base class for loggers that flush logs in background.
    """

    __slots__ = ("_enabled", "_queue", "_background_flusher", "_flush_period")

    def __init__(self, flush_period: int = 1, **kwargs: Any) -> None:
        """Initialize logger.

        Args:
            flush_period: The background task will flush all log events in queue at
                this period.
        """
        LoggerBase.__init__(self, **kwargs)
        self._enabled = False
        self._flush_period = flush_period

    def __del__(self) -> None:
        self._enabled = False

    def _check_ready(self) -> None:
        """Check if the logger is ready to emit events.

        Raises:
            LoggerNotReadyException if not ready.
        """
        if not self._enabled:
            raise LoggerNotReadyException("Logger not initialized or already closed.")

    @abstractmethod
    def _emit(self, event: LogEvent) -> None:
        """Emit log event.

        Args:
            event: Log event.
        """
