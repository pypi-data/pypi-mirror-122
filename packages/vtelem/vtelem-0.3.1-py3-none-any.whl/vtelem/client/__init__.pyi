from queue import Queue
from typing import Any, List
from vtelem.channel.registry import ChannelRegistry as ChannelRegistry
from vtelem.classes.type_primitive import TypePrimitive as TypePrimitive
from vtelem.frame.processor import FrameProcessor as FrameProcessor
from vtelem.mtu import DEFAULT_MTU as DEFAULT_MTU
from vtelem.parsing.encapsulation import decode_frame as decode_frame

LOG: Any

class TelemetryClient:
    name: Any
    mtu: Any
    channel_registry: Any
    frames: Any
    expected_id: Any
    processor: Any
    def __init__(self, name: str, output_stream: Queue, channel_registry: ChannelRegistry, app_id: TypePrimitive = ..., mtu: int = ...) -> None: ...
    def update_mtu(self, new_mtu: int) -> None: ...
    def handle_frames(self, new_frames: List[bytes]) -> int: ...
