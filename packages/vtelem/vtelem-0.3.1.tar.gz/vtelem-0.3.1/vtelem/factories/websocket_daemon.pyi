from vtelem.classes.time_keeper import TimeKeeper as TimeKeeper
from vtelem.daemon.command_queue import CommandQueueDaemon as CommandQueueDaemon
from vtelem.daemon.websocket import WebsocketDaemon as WebsocketDaemon
from vtelem.mtu import Host as Host
from vtelem.telemetry.environment import TelemetryEnvironment as TelemetryEnvironment

def commandable_websocket_daemon(name: str, daemon: CommandQueueDaemon, address: Host = ..., env: TelemetryEnvironment = ..., keeper: TimeKeeper = ...) -> WebsocketDaemon: ...
