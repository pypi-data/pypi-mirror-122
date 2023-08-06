from queue import Queue
from typing import Any, List, Tuple
from vtelem.channel import Channel as Channel
from vtelem.channel.registry import ChannelRegistry as ChannelRegistry
from vtelem.classes.event_queue import EventQueue as EventQueue
from vtelem.classes.time_entity import OptionalRLock as OptionalRLock
from vtelem.enums.primitive import Primitive as Primitive
from vtelem.frame import Frame as Frame
from vtelem.frame.channel import ChannelFrame as ChannelFrame
from vtelem.frame.framer import Framer as Framer

LOG: Any

class ChannelFramer(Framer):
    registry: Any
    channels: Any
    lock: Any
    def __init__(self, mtu: int, registry: ChannelRegistry, channels: List[Channel], channel_lock: OptionalRLock, app_id_basis: float = ..., use_crc: bool = ...) -> None: ...
    def new_event_frame(self, time: float = ...) -> ChannelFrame: ...
    def new_data_frame(self, time: float = ...) -> ChannelFrame: ...
    def add_channel(self, channel: Channel) -> None: ...
    def build_event_frames(self, time: float, event_queue: EventQueue, queue: Queue, write_crc: bool = ...) -> Tuple[int, int]: ...
    def build_data_frames(self, time: float, queue: Queue, write_crc: bool = ...) -> Tuple[int, int]: ...

def build_dummy_frame(overall_size: int, app_id_basis: float = ..., bad_crc: bool = ...) -> Frame: ...
