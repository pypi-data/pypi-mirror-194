"""Asyncio Logger base."""
from __future__ import annotations
from abc import abstractmethod
from asyncio import CancelledError, create_task, Queue, QueueEmpty, shield, sleep
from typing import Any, Callable, Awaitable
from jhalog._base import BackgroundLoggerBase
from jhalog._event import LogEvent


class AsyncBackgroundLoggerBase(BackgroundLoggerBase):
    """AsyncIO Logger base class."""

    def __init__(self, **kwargs: Any) -> None:
        BackgroundLoggerBase.__init__(self, **kwargs)
        self._queue: Queue[LogEvent] = Queue()
        self._background_flusher: Awaitable[Callable[[], None]] | None = None

    async def __aenter__(self) -> "AsyncBackgroundLoggerBase":
        self._set_default_server_field(await self._async_get_server_id())
        await self._start_backend()
        self._background_flusher = create_task(self._flusher())  # type: ignore
        self._enabled = True
        return self

    async def __aexit__(self, *_: Any) -> None:
        self.emit_shutdown_completed_event()
        self._enabled = False
        if self._background_flusher is not None:
            await self._background_flusher
        await self._stop_backend()

    def __enter__(self) -> "AsyncBackgroundLoggerBase":
        raise TypeError('This logger must be initialized with "__aenter__".')

    @abstractmethod
    async def _flush_multiple_events(self, event: LogEvent) -> None:
        """Flush multiple log events.

        Args:
            event: Initial log event.
        """
        # This method should get the first event from the "event" argument
        # and gather all remaining events in the queue until empty.
        # Then, this method should flush all these events.
        # Once all events are flushed, this method should return.

    @abstractmethod
    async def _start_backend(self) -> None:
        """Initialize backend."""

    @abstractmethod
    async def _stop_backend(self) -> None:
        """Terminate backend."""

    def _emit(self, event: LogEvent) -> None:
        """Put in queue.

        Args:
            event: Log event.
        """
        self._queue.put_nowait(event)

    async def _flush(self) -> None:
        """Flush log events."""
        try:
            event = self._queue.get_nowait()
        except QueueEmpty:
            return
        await shield(self._flush_multiple_events(event))

    async def _flusher(self) -> None:
        """Flush log events in background."""
        try:
            while self._enabled or not self._queue.empty():
                await self._flush()
                await sleep(self._flush_period)
        except CancelledError:
            while not self._queue.empty():
                await self._flush()

    async def _async_get_server_id(self) -> str:
        """Get server identifier.

        The value should uniquely identify the server.

        Returns:
            Server identifier.
        """
        return self._get_server_id()
