from typing import Any, FrozenSet
from vtelem.classes.serdes import Serializable as Serializable
from vtelem.enums.primitive import Primitive as Primitive, get_name as get_name, to_dict as to_dict
from vtelem.types.serializable import ObjectData as ObjectData

class SerializablePrimitive(Serializable):
    primitive: Any
    def init(self, data: ObjectData) -> None: ...

def from_primitive(prim: Primitive, **kwargs) -> SerializablePrimitive: ...
def get_all(**kwargs) -> FrozenSet[SerializablePrimitive]: ...
