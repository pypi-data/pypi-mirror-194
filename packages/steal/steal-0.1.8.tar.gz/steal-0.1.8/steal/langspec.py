import json
import importlib.resources
import steal

from enum import Enum
from typing import Dict, List, Generic, TypeVar, Tuple, Optional
from dataclasses import dataclass



class StackTypeEnum(str, Enum):
    ADDR = 'addr'
    BYTEARRAY = "[]byte"
    ANY = 'any'
    BIGINT = 'bigint'
    BOOL = 'bool'
    HASH = 'hash'
    KEY = 'key'
    method = 'method'
    NONE = 'none'
    UINT64 = 'uint64'

@dataclass
class StackType:
    type: StackTypeEnum
    length_bound: Optional[Tuple[int, int]]
    value_bound: Optional[Tuple[int, int]]

    @classmethod
    def from_spec(cls, spec: Dict):
        return StackType(type=StackTypeEnum(spec['Type']),
                         length_bound=spec.get('LengthBound'),
                         value_bound=spec.get('ValueBound'))

    def __str__(self) -> str:
        return self.type.value


@dataclass
class FieldEnum:
    name: str
    type: StackTypeEnum
    note: str
    value: int

    @classmethod
    def from_spec(cls, spec: Dict):
        return FieldEnum(name=spec['Name'],
                         type=StackTypeEnum(spec['Type']),
                         note=spec.get('Note'),
                         value=spec['Value'])

    def __str__(self) -> str:
        return self.name

@dataclass
class Field:
    name: str
    enums: Dict[str, FieldEnum]

# Should we consider lazy loading for the below?
langspec = json.loads(importlib.resources.read_text(package=steal,
                                                    resource="langspec.json"))
stack_types = {k: StackType.from_spec(spec) for k, spec in langspec['StackTypes'].items()}
fields = {k: Field(k, {spec["Name"]: FieldEnum.from_spec(spec) for spec in v}) for k, v in langspec['Fields'].items()}

@dataclass
class ImmediateArg:
    name: str
    comment: str
    encoding: str
    reference: Optional[Field]

    @classmethod
    def from_spec(cls, spec: Dict):
        return ImmediateArg(name=spec['Name'],
                            comment=spec['Comment'],
                            encoding=spec['Encoding'],
                            reference=spec.get('Reference'))

    def __str__(self) -> str:
        return self.name

T = TypeVar('T')
@dataclass
class Opcode(Generic[T]):

    name: str
    size: int
    cost: int
    doc: Optional[str]
    opcode: Optional[str]
    doc_extra: Optional[str]
    groups: List[str]
    args: Optional[List[StackType]]
    returns: Optional[List[StackType]]
    immediate_args: Optional[List[ImmediateArg]]

    def __str__(self) -> str:
        return '{}'.format(self.name)
    
    @classmethod
    def from_spec(cls, spec: Dict) -> T:
        immediate_args = None
        if 'ImmediateDetails' in spec:
            immediate_args = []
            for arg_spec in spec['ImmediateDetails']:
                immediate_args.append(ImmediateArg.from_spec(arg_spec))

        args = None
        if 'Args' in spec:
            args = [stack_types[t] for t in spec['Args']]

        returns = None
        if 'Returns' in spec:
            returns = [stack_types[t] for t in spec['Returns']]

        return Opcode(
            name=spec['Name'],
            size=spec['Size'],
            cost=spec['Cost'],
            doc=spec.get('Doc'),
            opcode=spec.get('Opcode'),
            doc_extra=spec.get('DocExtra'),
            groups=spec.get('Groups'),
            args=args,
            returns=returns,
            immediate_args=immediate_args,
        )

opcodes = {spec['Name']: Opcode.from_spec(spec) for spec in langspec['Ops']}
opcodes.update({spec['Name']: Opcode.from_spec(spec) for spec in langspec['PseudoOps']})