from typing import Any
from vtelem.daemon.command_queue import CommandQueueDaemon as CommandQueueDaemon
from vtelem.daemon.telemetry import TelemetryDaemon as TelemetryDaemon
from vtelem.registry import DEFAULT_INDENT as DEFAULT_INDENT

def register_http_handlers(server: Any, telem: TelemetryDaemon, cmd: CommandQueueDaemon) -> None: ...
