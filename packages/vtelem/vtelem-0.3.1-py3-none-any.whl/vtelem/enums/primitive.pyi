from enum import Enum
from json import JSONEncoder
from typing import Any, Callable, NamedTuple, Tuple, Type, Union
from vtelem.types.serializable import ObjectData as ObjectData

PrimitiveValue = Union[int, float, bool]

class BasePrimitive(NamedTuple):
    fmt: str
    type: Type
    size: int
    name: str
    signed: bool
    min: int
    max: int
    validate: Callable[[Any, int], bool]

def integer_bounds(byte_count: int, signed: bool) -> Tuple[int, int]: ...
def integer_can_hold(prim: BasePrimitive, val: int) -> bool: ...

class Primitive(Enum):
    BOOLEAN: Any
    INT8: Any
    UINT8: Any
    INT16: Any
    UINT16: Any
    INT32: Any
    UINT32: Any
    INT64: Any
    UINT64: Any
    FLOAT: Any
    DOUBLE: Any

def random_integer(prim: Primitive) -> int: ...
def get_name(inst: Primitive) -> str: ...
def get_fstring(inst: Primitive) -> str: ...
def get_size(inst: Primitive) -> int: ...
def default_val(inst: Primitive) -> PrimitiveValue: ...

INTEGER_PRIMITIVES: Any

def to_dict(prim: Primitive) -> ObjectData: ...

class PrimitiveEncoder(JSONEncoder):
    def default(self, o) -> dict: ...
