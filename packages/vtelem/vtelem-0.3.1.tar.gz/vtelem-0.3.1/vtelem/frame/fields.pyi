from typing import List, NamedTuple
from vtelem.classes import DEFAULTS as DEFAULTS
from vtelem.types.frame import FieldType as FieldType, MessageType as MessageType

MESSAGE_FIELDS: List[FieldType]

class ParsedMessage(NamedTuple):
    type: MessageType
    number: int
    crc: int
    fragment_index: int
    total_fragments: int
    data: bytes

def to_parsed(data: dict) -> ParsedMessage: ...
