import socket
from enum import IntEnum
from typing import Any, NamedTuple
from vtelem.channel.framer import build_dummy_frame as build_dummy_frame
from vtelem.frame import FRAME_OVERHEAD as FRAME_OVERHEAD

LOG: Any

def mtu_to_usable(mtu: int, medium_overhead: int = ...) -> int: ...

DEFAULT_MTU: Any

class Host(NamedTuple):
    address: str
    port: int

class SocketConstants(IntEnum):
    IP_MTU: int
    IP_MTU_DISCOVER: int
    IP_PMTUDISC_DO: int

def create_udp_socket(host: Host, is_client: bool = ...) -> socket.SocketType: ...
def discover_mtu(sock: socket.SocketType, probe_size: int = ..., app_id_basis: float = ...) -> int: ...
def get_free_port(kind: IntEnum, interface_ip: str = ..., test_port: int = ...) -> int: ...
def host_resolve_zero(kind: IntEnum, host: Host) -> Host: ...
def get_free_tcp_port(interface_ip: str = ..., test_port: int = ...) -> int: ...
def discover_ipv4_mtu(host: Host, probe_size: int = ...) -> int: ...
