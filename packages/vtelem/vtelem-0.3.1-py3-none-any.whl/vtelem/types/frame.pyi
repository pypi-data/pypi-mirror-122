from enum import IntEnum
from typing import Any, NamedTuple, Optional
from vtelem.classes.user_enum import from_enum as from_enum
from vtelem.enums.primitive import Primitive as Primitive

class FrameType(IntEnum):
    INVALID: int
    DATA: int
    EVENT: int
    MESSAGE: int
    STREAM: int

class FrameHeader(NamedTuple):
    length: int
    app_id: int
    type: FrameType
    timestamp: int
    size: int

class FrameFooter(NamedTuple):
    crc: Optional[int]

class ParsedFrame(NamedTuple):
    header: FrameHeader
    body: dict
    footer: FrameFooter

class FieldType(NamedTuple):
    name: str
    type: Primitive

class MessageType(IntEnum):
    AGNOSTIC: int
    TEXT: int
    JSON: int
    ENUM: int
    ENUM_REGISTRY: int
    PRIMITIVE: int

MESSAGE_TYPES: Any
