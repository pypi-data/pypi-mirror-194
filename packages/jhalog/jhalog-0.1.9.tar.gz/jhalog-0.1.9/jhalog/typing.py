"""Specials types."""
from __future__ import annotations
from datetime import datetime as _datetime
from typing import Literal as _Literal, TypedDict as _TypedDict, Any as _Any

HttpMethod = _Literal["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]  # noqa
EventLevel = _Literal["debug", "info", "warning", "error", "critical"]  # noqa


class Fields(_TypedDict, total=False):
    """Log event fields."""

    client_id: str
    client_ip: str
    client_jti: str
    client_type: str
    client_user_agent: str
    created: list[_Any]
    date: _datetime
    error_detail: _Any
    execution_time: float
    id: str
    level: EventLevel
    method: HttpMethod
    os_uptime: float
    path: str
    server_id: str
    server_version: str
    server_uptime: float
    status_code: int
    type: str
