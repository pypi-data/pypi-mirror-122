from pathlib import Path
from queue import Queue
from typing import Any, Iterator, NamedTuple, Optional, Tuple
from vtelem.channel.registry import ChannelRegistry as ChannelRegistry
from vtelem.classes.type_primitive import TypePrimitive as TypePrimitive, new_default as new_default
from vtelem.client import TelemetryClient as TelemetryClient
from vtelem.daemon import DaemonBase as DaemonBase, DaemonState as DaemonState
from vtelem.mtu import DEFAULT_MTU as DEFAULT_MTU
from vtelem.stream.writer import StreamWriter as StreamWriter
from vtelem.telemetry.environment import TelemetryEnvironment as TelemetryEnvironment

LOG: Any
TELEM_SUFFIX: str

class FileDecodeTask(NamedTuple):
    path: Path
    byte_index: int
    max_frames: Optional[int]

class FileClient(DaemonBase, TelemetryClient):
    task: Any
    frame_count: int
    to_process: Any
    def __init__(self, task: FileDecodeTask, output_stream: Queue, channel_registry: ChannelRegistry, app_id: TypePrimitive = ..., env: TelemetryEnvironment = ..., mtu: int = ...) -> None: ...
    def process_raw_frames(self, task: FileDecodeTask) -> bool: ...
    def run(self, *_, **__) -> None: ...

def create(writer: StreamWriter, env: TelemetryEnvironment, mtu: int = ..., max_frames: int = ...) -> Iterator[Tuple[FileClient, Queue]]: ...
