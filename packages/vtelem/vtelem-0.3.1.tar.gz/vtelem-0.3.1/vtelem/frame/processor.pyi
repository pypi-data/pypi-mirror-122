from typing import Any, List
from vtelem.classes.byte_buffer import ByteBuffer as ByteBuffer
from vtelem.classes.type_primitive import TypePrimitive as TypePrimitive

class FrameProcessor:
    buffer: Any
    size: int
    size_stale: bool
    def __init__(self) -> None: ...
    def read_size(self, frame_size: TypePrimitive, mtu: int) -> None: ...
    def process(self, data: bytes, frame_size: TypePrimitive, mtu: int) -> List[bytes]: ...
