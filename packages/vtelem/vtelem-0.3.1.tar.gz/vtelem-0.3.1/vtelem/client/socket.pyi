from queue import Queue
from socket import SocketType as SocketType
from typing import Any, Callable
from vtelem.channel.registry import ChannelRegistry as ChannelRegistry
from vtelem.classes.type_primitive import TypePrimitive as TypePrimitive, new_default as new_default
from vtelem.client import TelemetryClient as TelemetryClient
from vtelem.daemon import DaemonBase as DaemonBase, DaemonState as DaemonState
from vtelem.mtu import DEFAULT_MTU as DEFAULT_MTU
from vtelem.telemetry.environment import TelemetryEnvironment as TelemetryEnvironment

LOG: Any

class SocketClient(DaemonBase, TelemetryClient):
    socket: Any
    def __init__(self, sock: SocketType, stopper: Callable, output_stream: Queue, channel_registry: ChannelRegistry, app_id: TypePrimitive = ..., env: TelemetryEnvironment = ..., mtu: int = ...) -> None: ...
    name: Any
    def update_name(self, sock: SocketType) -> None: ...
    def close(self) -> None: ...
    def run(self, *_, **__) -> None: ...
