from typing import Any, Callable, Dict
from vtelem.channel.registry import ChannelRegistry as ChannelRegistry
from vtelem.classes.byte_buffer import ByteBuffer as ByteBuffer
from vtelem.classes.user_enum import from_enum as from_enum
from vtelem.parsing.frames import parse_data_frame as parse_data_frame, parse_event_frame as parse_event_frame, parse_invalid_frame as parse_invalid_frame, parse_message_frame as parse_message_frame, parse_stream_frame as parse_stream_frame
from vtelem.types.frame import FrameHeader as FrameHeader, FrameType as FrameType

FrameParser = Callable[[FrameHeader, ByteBuffer, ChannelRegistry], dict]
PARSERS: Dict[FrameType, FrameParser]
FRAME_TYPES: Any
