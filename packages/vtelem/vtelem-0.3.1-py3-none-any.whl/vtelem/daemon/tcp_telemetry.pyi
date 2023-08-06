import socketserver
from queue import Queue
from typing import Any, Tuple
from vtelem.client.tcp import TcpClient as TcpClient
from vtelem.daemon import DaemonBase as DaemonBase
from vtelem.mtu import DEFAULT_MTU as DEFAULT_MTU, Host as Host
from vtelem.stream.writer import QueueClientManager as QueueClientManager, StreamWriter as StreamWriter
from vtelem.telemetry.environment import TelemetryEnvironment as TelemetryEnvironment

LOG: Any

class TcpTelemetryHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None: ...

class TcpTelemetryDaemon(QueueClientManager, DaemonBase):
    server: Any
    client_sems: Any
    def __init__(self, name: str, writer: StreamWriter, env: TelemetryEnvironment, address: Host = ..., time_keeper: Any = ...) -> None: ...
    def client(self, mtu: int = ...) -> Tuple[TcpClient, Queue]: ...
    @property
    def address(self) -> Tuple[str, int]: ...
    def run(self, *_, **__) -> None: ...
