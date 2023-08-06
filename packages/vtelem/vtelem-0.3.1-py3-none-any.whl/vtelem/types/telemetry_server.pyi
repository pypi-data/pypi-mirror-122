from typing import Any, Callable, Dict, List, NamedTuple, Optional
from vtelem.channel.group_registry import ChannelGroupRegistry as ChannelGroupRegistry
from vtelem.mtu import Host as Host

AppSetup = Callable[[ChannelGroupRegistry, Dict[str, Any]], None]
AppLoop = Callable[[ChannelGroupRegistry, Dict[str, Any]], None]

class Service(NamedTuple):
    name: str
    host: Optional[Host]
    enabled: bool

class TelemetryServices(NamedTuple):
    http: Service
    websocket_cmd: Service
    websocket_tlm: Service
    tcp_tlm: Service
    udp: Optional[List[Host]]

def default_services(**kwargs: Service) -> TelemetryServices: ...
