from typing import Any, Tuple
from vtelem.classes.metered_queue import create as create
from vtelem.daemon.queue import QueueDaemon as QueueDaemon
from vtelem.registry import DEFAULT_INDENT as DEFAULT_INDENT
from vtelem.telemetry.environment import TelemetryEnvironment as TelemetryEnvironment
from vtelem.types.command_queue_daemon import ConsumerType as ConsumerType, HandlersType as HandlersType, ResultCbType as ResultCbType

LOG: Any

class CommandQueueDaemon(QueueDaemon):
    handlers: Any
    def __init__(self, name: str, env: TelemetryEnvironment = ..., time_keeper: Any = ...): ...
    def register_consumer(self, command: str, handler: ConsumerType, result_cb: ResultCbType = ..., help_msg: str = ...) -> None: ...
    def enqueue(self, command: Any, result_cb: ResultCbType = ...) -> None: ...
    def execute(self, command: Any) -> Tuple[bool, str]: ...
