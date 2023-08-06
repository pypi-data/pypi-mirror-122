from typing import List, Tuple
from vtelem.registry import Registry as Registry

Service = List[Tuple[str, int]]

class ServiceRegistry(Registry[Service]):
    def __init__(self, initial_services: List[Tuple[str, Service]] = ...) -> None: ...
