from typing import Any, Callable, Optional
from vtelem.daemon.event_loop import EventLoopDaemon as EventLoopDaemon
from vtelem.mtu import Host as Host, get_free_tcp_port as get_free_tcp_port
from vtelem.registry.service import ServiceRegistry as ServiceRegistry
from vtelem.telemetry.environment import TelemetryEnvironment as TelemetryEnvironment

LOG: Any

def create_default_handler(message_consumer: Callable) -> Callable: ...

class WebsocketDaemon(EventLoopDaemon):
    address: Any
    secure: Any
    server: Any
    serving: bool
    def __init__(self, name: str, message_consumer: Optional[Callable], address: Host = ..., env: TelemetryEnvironment = ..., time_keeper: Any = ..., ws_handler: Callable = ..., secure: bool = ...) -> None: ...
