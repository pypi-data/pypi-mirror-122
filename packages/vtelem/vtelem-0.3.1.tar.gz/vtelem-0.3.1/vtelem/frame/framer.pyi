from typing import Any, Callable, Dict, Type
from vtelem.classes import DEFAULTS as DEFAULTS
from vtelem.classes.type_primitive import TypePrimitive as TypePrimitive, new_default as new_default
from vtelem.enums.frame import FRAME_TYPES as FRAME_TYPES
from vtelem.enums.primitive import random_integer as random_integer
from vtelem.frame import Frame as Frame, time_to_int as time_to_int
from vtelem.frame.channel import ChannelFrame as ChannelFrame
from vtelem.frame.message import MessageFrame as MessageFrame

LOG: Any
FRAME_CLASS_MAP: Dict[str, Type]

def basis_to_int(basis: float) -> int: ...

class Framer:
    mtu: Any
    timestamp: Any
    frame_types: Any
    timestamps: Any
    primitives: Any
    use_crc: Any
    def __init__(self, mtu: int, app_id_basis: float = ..., use_crc: bool = ...) -> None: ...
    def new_frame(self, frame_type: str, time: float = ...) -> Frame: ...
    @staticmethod
    def create_app_id(basis: float = ...) -> TypePrimitive: ...

def build_dummy_frame(overall_size: int, frame_type: str = ..., frame_builder: Callable[[Frame], None] = ..., app_id_basis: float = ..., bad_crc: bool = ...) -> ChannelFrame: ...
