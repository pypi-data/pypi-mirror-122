from queue import Queue
from typing import Any, Callable
from vtelem.daemon import DaemonBase as DaemonBase
from vtelem.telemetry.environment import TelemetryEnvironment as TelemetryEnvironment

class QueueDaemon(DaemonBase):
    queue: Any
    handle: Any
    def __init__(self, name: str, input_stream: Queue, elem_handle: Callable, env: TelemetryEnvironment = ..., time_keeper: Any = ...) -> None: ...
    def await_empty(self, interval: float = ...) -> None: ...
    def run(self, *_, **__) -> None: ...
