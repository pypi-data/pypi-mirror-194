"""Exceptions."""


class JhalogException(Exception):
    """Jhalog base exception."""


class LogEventNotFoundException(JhalogException):
    """Log event not found."""


class LogEventAlreadyEmittingException(JhalogException):
    """Log event already emitting."""


class LoggerNotReadyException(JhalogException):
    """Logger not initialized or already closed."""
