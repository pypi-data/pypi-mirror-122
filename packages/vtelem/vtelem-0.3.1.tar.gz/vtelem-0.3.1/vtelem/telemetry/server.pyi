from typing import Any, Iterator
from vtelem.channel.group_registry import ChannelGroupRegistry as ChannelGroupRegistry
from vtelem.classes.http_request_mapper import MapperAwareRequestHandler as MapperAwareRequestHandler
from vtelem.classes.time_keeper import TimeKeeper as TimeKeeper
from vtelem.classes.udp_client_manager import UdpClientManager as UdpClientManager
from vtelem.daemon import DaemonOperation as DaemonOperation
from vtelem.daemon.command_queue import CommandQueueDaemon as CommandQueueDaemon
from vtelem.daemon.http import HttpDaemon as HttpDaemon
from vtelem.daemon.manager import DaemonManager as DaemonManager
from vtelem.daemon.synchronous import Daemon as Daemon
from vtelem.daemon.tcp_telemetry import TcpTelemetryDaemon as TcpTelemetryDaemon
from vtelem.daemon.telemetry import TelemetryDaemon as TelemetryDaemon
from vtelem.daemon.websocket_telemetry import WebsocketTelemetryDaemon as WebsocketTelemetryDaemon
from vtelem.factories.daemon_manager import create_daemon_manager_commander as create_daemon_manager_commander
from vtelem.factories.telemetry_environment import create_channel_commander as create_channel_commander
from vtelem.factories.telemetry_server import register_http_handlers as register_http_handlers
from vtelem.factories.udp_client_manager import create_udp_client_commander as create_udp_client_commander
from vtelem.factories.websocket_daemon import commandable_websocket_daemon as commandable_websocket_daemon
from vtelem.mtu import DEFAULT_MTU as DEFAULT_MTU, Host as Host, discover_ipv4_mtu as discover_ipv4_mtu, mtu_to_usable as mtu_to_usable
from vtelem.registry.service import ServiceRegistry as ServiceRegistry
from vtelem.stream.writer import StreamWriter as StreamWriter
from vtelem.types.telemetry_server import AppLoop as AppLoop, AppSetup as AppSetup, TelemetryServices as TelemetryServices, default_services as default_services

class TelemetryServer(HttpDaemon):
    daemons: Any
    state_sem: Any
    first_start: bool
    time_keeper: Any
    channel_groups: Any
    udp_clients: Any
    http_enabled: Any
    def __init__(self, tick_length: float, telem_rate: float, metrics_rate: float = ..., app_id_basis: float = ..., services: TelemetryServices = ...) -> None: ...
    def register_application(self, name: str, rate: float, setup: AppSetup, loop: AppLoop) -> bool: ...
    def scale_speed(self, scalar: float) -> None: ...
    def start_all(self) -> None: ...
    def stop_all(self) -> None: ...
    def booted(self, *_, **__) -> Iterator[None]: ...
    def await_shutdown(self, timeout: float = ...) -> None: ...
