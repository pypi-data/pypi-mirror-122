from queue import Queue
from vtelem.channel.registry import ChannelRegistry as ChannelRegistry
from vtelem.classes.type_primitive import TypePrimitive as TypePrimitive
from vtelem.client.socket import SocketClient as SocketClient
from vtelem.mtu import DEFAULT_MTU as DEFAULT_MTU, Host as Host, host_resolve_zero as host_resolve_zero
from vtelem.telemetry.environment import TelemetryEnvironment as TelemetryEnvironment

class TcpClient(SocketClient):
    def __init__(self, host: Host, output_stream: Queue, channel_registry: ChannelRegistry, app_id: TypePrimitive = ..., env: TelemetryEnvironment = ..., mtu: int = ...): ...
