from typing import Dict, List, Union

ObjectKey = Union[int, str]
ObjectElement = Union[float, int, str, bool, None]
ObjectMap = Dict[ObjectKey, ObjectElement]
ObjectData = Dict[ObjectKey, Union[ObjectElement, List[ObjectElement], ObjectMap]]
