"""Threaded logger base."""
from abc import abstractmethod
from queue import Queue, Empty
from time import sleep
from typing import Any
from threading import Thread
from jhalog._base import BackgroundLoggerBase
from jhalog._event import LogEvent


class ThreadBackgroundLoggerBase(BackgroundLoggerBase):
    """Threaded background logger base class."""

    def __init__(self, **kwargs: Any) -> None:
        BackgroundLoggerBase.__init__(self, **kwargs)
        self._set_default_server_field()
        self._start_backend()
        self._queue: Queue[LogEvent] = Queue()
        self._background_flusher = Thread(target=self._flusher)
        self._background_flusher.run()
        self._enabled = True

    def __exit__(self, *_: Any) -> None:
        self.emit_shutdown_completed_event()
        self._enabled = False
        self._background_flusher.join()
        self._stop_backend()

    @abstractmethod
    def _flush_multiple_events(self, event: LogEvent) -> None:
        """Flush multiple log events.

        Args:
            event: Initial log event.
        """
        # This method should get the first event from the "event" argument
        # and gather all remaining events in the queue until empty.
        # Then, this method should flush all these events.
        # Once all events are flushed, this method should return.

    @abstractmethod
    def _start_backend(self) -> None:
        """Initialize backend."""

    @abstractmethod
    def _stop_backend(self) -> None:
        """Terminate backend."""

    def _emit(self, event: LogEvent) -> None:
        """Put in queue.

        Args:
            event: Log event.
        """
        self._queue.put_nowait(event)

    def _flush(self) -> None:
        """Flush log events."""
        try:
            event = self._queue.get_nowait()
        except Empty:
            return
        self._flush_multiple_events(event)

    def _flusher(self) -> None:
        """Flush log events in background."""
        while self._enabled or not self._queue.empty():
            self._flush()
            sleep(self._flush_period)
