from typing import Any
from vtelem.classes import DEFAULTS as DEFAULTS, EventType as EventType
from vtelem.classes.byte_buffer import ByteBuffer as ByteBuffer
from vtelem.classes.type_primitive import TypePrimitive as TypePrimitive, new_default as new_default
from vtelem.enums.primitive import Primitive as Primitive, get_size as get_size
from vtelem.frame import Frame as Frame, time_to_int as time_to_int

class ChannelFrame(Frame):
    elem_buffer: Any
    def __init__(self, mtu: int, frame_id: TypePrimitive, frame_type: TypePrimitive, timestamp: TypePrimitive, use_crc: bool = ...) -> None: ...
    initialized: bool
    def finalize_hook(self) -> None: ...
    def add_event(self, chan_id: int, chan_type: Primitive, prev: EventType, curr: EventType) -> bool: ...
    def add(self, chan_id: int, chan_type: Primitive, chan_val: Any) -> bool: ...
