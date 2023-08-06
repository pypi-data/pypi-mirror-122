from queue import Queue
from typing import Iterator, Tuple
from vtelem.channel.registry import ChannelRegistry as ChannelRegistry
from vtelem.classes.type_primitive import TypePrimitive as TypePrimitive
from vtelem.classes.udp_client_manager import UdpClientManager as UdpClientManager
from vtelem.client.socket import SocketClient as SocketClient
from vtelem.mtu import DEFAULT_MTU as DEFAULT_MTU, Host as Host, create_udp_socket as create_udp_socket, get_free_port as get_free_port, host_resolve_zero as host_resolve_zero
from vtelem.telemetry.environment import TelemetryEnvironment as TelemetryEnvironment

class UdpClient(SocketClient):
    def __init__(self, host: Host, output_stream: Queue, channel_registry: ChannelRegistry, app_id: TypePrimitive = ..., env: TelemetryEnvironment = ..., mtu: int = ...): ...

def create(manager: UdpClientManager, env: TelemetryEnvironment, test_port: int = ..., mtu: int = ..., local_addr: str = ...) -> Iterator[Tuple[UdpClient, Queue]]: ...
