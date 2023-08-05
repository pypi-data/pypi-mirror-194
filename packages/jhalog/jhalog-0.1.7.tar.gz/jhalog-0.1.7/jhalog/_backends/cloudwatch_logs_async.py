"""AWS CloudWatch Logs."""
from __future__ import annotations
from asyncio import gather, QueueEmpty
from typing import Any
from aioboto3 import Session
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectionError, ClientResponseError
from botocore.client import Config
from webuuid import Uuid
from jhalog._base_async import AsyncBackgroundLoggerBase
from jhalog._event import LogEvent
from jhalog._backends._cloudwatch_logs import CloudwatchLogsBase


class Logger(AsyncBackgroundLoggerBase, CloudwatchLogsBase):
    """Cloudwatch Logger."""

    def __init__(self, log_group_name: str, **kwargs: Any) -> None:
        """Initialize logger.

        Args:
            log_group_name: Cloudwatch Logs log group where to create the log stream
                where log event will be put. The log group must exist.
        """
        AsyncBackgroundLoggerBase.__init__(self, **kwargs)
        CloudwatchLogsBase.__init__(self, log_group_name=log_group_name)

    async def _flush_multiple_events(self, event: LogEvent) -> None:
        """Flush multiple log events.

        Use a single or multiple requests to put log events and handle Cloudwatch logs
        limits.

        Args:
            event: Initial log event.
        """
        log_events = [self._format_log_event(event)]
        self._queue.task_done()
        tasks = []
        while log_events:
            size = self._get_log_event_size(log_events[0])
            next_log_events = []
            while True:
                try:
                    log = self._format_log_event(self._queue.get_nowait())
                except QueueEmpty:
                    break
                self._queue.task_done()
                log_events.append(log)
                size += self._get_log_event_size(log)
                if (
                    size > self._BATCH_SIZE_LIMIT
                    or len(log_events) > self._BATCH_COUNT_LIMIT
                ):
                    next_log_events.append(log_events.pop())
                    break
            tasks.append(
                self._client.put_log_events(logEvents=log_events, **self._client_kwargs)
            )
            log_events = next_log_events
        await gather(*tasks)

    async def _start_backend(self) -> None:
        """Start _backends."""
        self._client = (
            await Session()
            .client(
                "logs",
                config=Config(
                    parameter_validation=False,
                    retries=dict(
                        mode="standard", max_attempts=self._RETRIES_MAX_ATTEMPTS
                    ),
                ),
            )
            .__aenter__()
        )
        self._client_kwargs["logStreamName"] = (
            f"{self._default_fields['server_id']}-{Uuid().base64()}"
        )
        await self._client.create_log_stream(**self._client_kwargs)

    async def _stop_backend(self) -> None:
        """Stop _backends."""
        await self._client.__aexit__(None, None, None)

    async def _async_get_server_id(self) -> str:
        """Get server identifier.

        If on an AWS EC2 instance, get the instance ID using IMDSv2.

        Returns:
            Server identifier.
        """
        try:
            async with ClientSession("http://169.254.169.254") as http:
                async with http.put(
                    "/latest/api/token",
                    headers={"X-aws-ec2-metadata-token-ttl-seconds": "60"},
                    raise_for_status=True,
                ) as response:
                    token = await response.text()
                async with http.get(
                    "/latest/meta-data/instance-id",
                    headers={"X-aws-ec2-metadata-token": token},
                    raise_for_status=True,
                ) as response:
                    return await response.text()
        except (ClientConnectionError, ClientResponseError):
            return await super()._async_get_server_id()
