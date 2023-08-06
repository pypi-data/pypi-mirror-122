from typing import Any
from vtelem.daemon import DaemonBase as DaemonBase
from vtelem.telemetry.environment import TelemetryEnvironment as TelemetryEnvironment

class EventLoopDaemon(DaemonBase):
    eloop: Any
    wait_count: int
    wait_poster: Any
    def __init__(self, name: str, env: TelemetryEnvironment = ..., time_keeper: Any = ..., stop_grace: float = ...) -> None: ...
    def run(self, *args, **kwargs) -> None: ...
