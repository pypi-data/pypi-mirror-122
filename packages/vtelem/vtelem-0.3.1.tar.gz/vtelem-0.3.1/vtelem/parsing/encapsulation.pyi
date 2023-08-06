from typing import Any, Optional, Tuple
from vtelem.channel.registry import ChannelRegistry as ChannelRegistry
from vtelem.classes import DEFAULTS as DEFAULTS
from vtelem.classes.byte_buffer import ByteBuffer as ByteBuffer
from vtelem.classes.type_primitive import TypePrimitive as TypePrimitive
from vtelem.enums.frame import PARSERS as PARSERS
from vtelem.enums.primitive import get_size as get_size
from vtelem.types.frame import FrameFooter as FrameFooter, FrameHeader as FrameHeader, FrameType as FrameType, ParsedFrame as ParsedFrame

LOG: Any

def parse_frame_header(buf: ByteBuffer, expected_id: Optional[TypePrimitive] = ...) -> Tuple[int, Optional[FrameHeader]]: ...
def parse_frame_footer(buf: ByteBuffer) -> FrameFooter: ...
def decode_frame(channel_registry: ChannelRegistry, data: bytes, size: int, expected_id: Optional[TypePrimitive] = ...) -> Optional[ParsedFrame]: ...
