from . import EventType as EventType
from .metered_queue import create as create
from typing import Any, List, Tuple

class EventQueue:
    queue: Any
    lock: Any
    def __init__(self) -> None: ...
    def enqueue(self, channel: str, prev: EventType, curr: EventType) -> bool: ...
    def consume(self) -> List[Tuple[str, EventType, EventType]]: ...
