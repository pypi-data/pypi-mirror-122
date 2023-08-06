from cerberus import Validator
from pathlib import Path
from typing import Dict

SchemaMap = Dict[str, Validator]

def load_schema(path: Path, **kwargs) -> Validator: ...
def load_schema_dir(path: Path, **kwargs) -> SchemaMap: ...
