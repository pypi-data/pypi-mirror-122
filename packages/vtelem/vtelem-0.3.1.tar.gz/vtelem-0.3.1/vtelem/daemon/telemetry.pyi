from typing import List
from vtelem.channel import Channel as Channel
from vtelem.classes.time_keeper import TimeKeeper as TimeKeeper
from vtelem.classes.user_enum import UserEnum as UserEnum
from vtelem.daemon.synchronous import Daemon as Daemon
from vtelem.telemetry.environment import TelemetryEnvironment as TelemetryEnvironment

class TelemetryDaemon(TelemetryEnvironment, Daemon):
    def __init__(self, name: str, mtu: int, rate: float, time_keeper: TimeKeeper, metrics_rate: float = ..., initial_channels: List[Channel] = ..., initial_enums: List[UserEnum] = ..., app_id_basis: float = ..., use_crc: bool = ...) -> None: ...
