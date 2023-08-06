from queue import Queue
from typing import Any, Optional

QUEUE_TIMEOUT: int

def queue_get(queue: Queue, timeout: int = ...) -> Optional[Any]: ...
def queue_get_none(queue: Queue, timeout: int = ...) -> None: ...
