"""Botocore exception handler."""
from __future__ import annotations
from botocore.exceptions import ClientError as _ClientError


def get_status_from_botocore_error(exception: BaseException) -> tuple[int, str] | None:
    """Return 503 "Unavailable" on AWS server side status codes.

    Args:
        exception: Exception.

    Returns:
        Status code, message
    """
    if isinstance(exception, _ClientError):
        status_code = int(exception.response["ResponseMetadata"]["HTTPStatusCode"])
        if status_code >= 500:
            return 503, "Unavailable"
        elif status_code == 429:
            return 429, "Too Many Requests"
    return None
