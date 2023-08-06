from queue import Queue
from typing import Any, Tuple
from vtelem.client.websocket import WebsocketClient as WebsocketClient
from vtelem.daemon.websocket import WebsocketDaemon as WebsocketDaemon
from vtelem.frame.channel import ChannelFrame as ChannelFrame
from vtelem.mtu import DEFAULT_MTU as DEFAULT_MTU, Host as Host
from vtelem.stream import queue_get as queue_get
from vtelem.stream.writer import QueueClientManager as QueueClientManager, StreamWriter as StreamWriter
from vtelem.telemetry.environment import TelemetryEnvironment as TelemetryEnvironment

class WebsocketTelemetryDaemon(QueueClientManager, WebsocketDaemon):
    def __init__(self, name: str, writer: StreamWriter, address: Host = ..., env: TelemetryEnvironment = ..., time_keeper: Any = ...) -> None: ...
    def client(self, mtu: int = ..., uri_path: str = ..., time_keeper: Any = ...) -> Tuple[WebsocketClient, Queue]: ...
