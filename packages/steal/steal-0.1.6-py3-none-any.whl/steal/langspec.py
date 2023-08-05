import json
import importlib.resources
import steal

from enum import Enum
from typing import Dict, List, Generic, TypeVar
from dataclasses import dataclass


langspec = json.loads(
    importlib.resources.read_text(package=steal, resource="langspec.json")
)

class StackType(Enum):
    UINT = 'U'
    BYTE = "B"
    ANY = '.'
@dataclass
class Arg:
    name: str
    arg_type: StackType

    def __repr__(self) -> str:
        return '{}({})'.format(self.arg_type.name, self.name)

T = TypeVar('T')
@dataclass
class Opcode(Generic[T]):

    opcode: str
    name: str
    size: int
    immediate_args: List[Arg]
    arg_types: List[StackType]
    return_types: List[StackType]

    def __repr__(self) -> str:
        return '{}'.format(self.name)
    
    @classmethod
    def from_spec(cls, spec: Dict) -> T:
        immediate_args = []
        enums = spec.get('ArgEnum', [])
        enum_types = spec.get('ArgEnumTypes', '.' * len(enums))
        for i, n in enumerate(enums):    
            immediate_arg = Arg(n, StackType(enum_types[i]))
            immediate_args.append(immediate_arg)

        arg_types = [StackType(t) for t in spec.get('Args', [])]
        return_types = [StackType(t) for t in spec.get('Returns', [])]
        return Opcode(
            spec['Opcode'],
            spec['Name'],
            spec['Size'],
            immediate_args,
            arg_types,
            return_types
        )

opcodes: Dict[str, Opcode] = {
    spec['Name']: Opcode.from_spec(spec) for spec in langspec['Ops']
}
