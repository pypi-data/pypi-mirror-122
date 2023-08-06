from queue import Queue
from typing import Any
from vtelem.channel.registry import ChannelRegistry as ChannelRegistry
from vtelem.classes.type_primitive import TypePrimitive as TypePrimitive, new_default as new_default
from vtelem.client import TelemetryClient as TelemetryClient
from vtelem.daemon import DaemonState as DaemonState
from vtelem.daemon.event_loop import EventLoopDaemon as EventLoopDaemon
from vtelem.mtu import DEFAULT_MTU as DEFAULT_MTU, Host as Host
from vtelem.telemetry.environment import TelemetryEnvironment as TelemetryEnvironment

LOG: Any

class WebsocketClient(EventLoopDaemon, TelemetryClient):
    connected: bool
    task: Any
    def __init__(self, host: Host, output_stream: Queue, channel_registry: ChannelRegistry, secure: bool = ..., uri_path: str = ..., app_id: TypePrimitive = ..., env: TelemetryEnvironment = ..., time_keeper: Any = ..., mtu: int = ...) -> None: ...
