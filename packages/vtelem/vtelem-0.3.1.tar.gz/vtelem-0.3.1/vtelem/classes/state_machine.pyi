from . import DEFAULTS as DEFAULTS
from .state import State as State
from .time_entity import LockEntity as LockEntity
from typing import Any, Iterator, List, Tuple
from vtelem.channel.group import ChannelGroup as ChannelGroup
from vtelem.telemetry.environment import TelemetryEnvironment as TelemetryEnvironment

LOG: Any

class StateMachine(LockEntity):
    states: Any
    current_state: Any
    name: Any
    metrics: Any
    def __init__(self, name: str, states: List[State], initial_state: State = ..., initial_data: dict = ..., env: TelemetryEnvironment = ..., rate: float = ...) -> None: ...
    def data(self) -> Iterator[dict]: ...
    def run(self, new_data: dict = ...) -> Tuple[State, State]: ...
