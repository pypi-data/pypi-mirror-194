import sys

from io import IOBase, StringIO
from typing import TypeVar, Generic, List, Generator, Optional
from dataclasses import dataclass, field

from steal import langspec
from steal.scanner import TokenType, Token

max_scratch_space = 256
scratch_space: List[str] = []


class ScratchSpaceOverFlowError(Exception):
    pass

def allocate_scratch_space(name: str) -> int:
    index = len(scratch_space)
    if index < max_scratch_space:
        scratch_space.append(name)
        return index
    return -1

def refer_scratch_space(name) -> int:
    try:
        return scratch_space.index(name)
    except:
        return -1

class CompilerError(Exception):
    
    def __init__(self, msg, token):
        super().__init__(msg)
        self.token = token

T = TypeVar('T')
@dataclass
class Node(Generic[T]):

    token: Token
    children: Optional[List[T]] = None
    immediate_args_override: Optional[List[str]] = None
    note: str = None

    def __post_init__(self):
        self.validate()

    def validate(self):
        pass

    @property
    def root(self) -> T:
        root = self
        while not root:
            root = self.parent
        return root

    @classmethod
    def from_tokens(cls, tokens: Generator[Token, None, None]) -> T:
        try:
            return cls._from_tokens(tokens)
        except CompilerError as e:
            print('Compiler error: {}'.format(str(e)), file=sys.stderr)
            print('Ln: {}, Col: {} Token: {}'.format(
                e.token.line, e.token.col, e.token.value
            ), file=sys.stderr)
            exit(1)

    @classmethod
    def _from_tokens(cls, tokens: Generator[Token, None, None],
                     head: Optional[Token] = None,
                     children: Optional[List[T]] = None) -> T:

        token = head or next(tokens)

        if token.token_type == TokenType.BEGIN:
            head = next(tokens)

            if head.token_type == TokenType.BEGIN:
                raise CompilerError('Invalid token', token=head)

            token = next(tokens)
            children = []
            while token.token_type != TokenType.END:
                child = Node._from_tokens(tokens, head=token)
                children.append(child)
                token = next(tokens)

            if token.token_type != TokenType.END:
                raise CompilerError('Unclosed expression', token=token)

            return Node._from_tokens(tokens, head=head, children=children)
        elif token.token_type == TokenType.ATOM:
            name = token.value.split('.')[0]
            if name in langspec.opcodes:
                opcode = langspec.opcodes[name]
                return Opcode(token,
                              children=children,
                              opcode=opcode)
            else:
                return Node(token=token, children=children)
        elif token.token_type == TokenType.VARIABLE:
            if children:
                index = allocate_scratch_space(token.value)
                if index < 0:
                    raise CompilerError('Scratch space overflow', token=token)

                return Opcode(token,
                            opcode=langspec.opcodes['store'],
                            immediate_args_override=[str(index)],
                            children=children,
                            note=token.value)
            else:
                index = refer_scratch_space(token.value)
                if index < 0:
                    raise CompilerError('Scratch space not found', token=token)

                return Opcode(token,
                              opcode=langspec.opcodes['load'],
                              immediate_args_override=[str(index)],
                              note=token.value)
        elif token.token_type == TokenType.BYTE:
            return Opcode(token, opcode=langspec.opcodes['byte'],
                          immediate_args_override=[token.value])
        elif token.token_type == TokenType.INT:
            return Opcode(token, opcode=langspec.opcodes['int'],
                          immediate_args_override=[token.value])
        elif token.token_type == TokenType.LABEL:
            return Label(token, children=children)
        elif token.token_type == TokenType.COMMENT:
            return Comment(token, children=children)

        raise CompilerError('Invalid token', token=token)

    @property
    def command(self):
        return self.token.head

    @property
    def immediate_args(self):
        return self.immediate_args_override or self.token.rest

    @property
    def statement(self):
        return ' '.join([self.command, *self.immediate_args])

    def emit(self):
        lines = []
        if self.children:
            for child in self.children:
                lines.extend(child.emit())
        statement = self.statement
        if self.note:
            lines.append('{} // {}'.format(statement, self.note))
        else:
            lines.append(statement)
        return lines

    def write(self, f: IOBase):
        f.writelines(['{}\n'.format(line) for line in self.emit()])

    def __str__(self) -> str:
        with StringIO() as io:
            self.write(io)
            return io.getvalue()

@dataclass
class Opcode(Node):

    opcode: langspec.Opcode = None

    @property
    def noncomment_children(self):
        if self.children:
            return [c for c in self.children if c.token.token_type != TokenType.COMMENT]
        return []

    @property
    def statement(self):
        return ' '.join([self.opcode.name, *self.immediate_args])

    def validate(self):

        if self.opcode.args:
            if len(self.noncomment_children) != len(self.opcode.args):
                raise CompilerError('Invalid number of stack args', token=self.token)

        if self.opcode.immediate_args:
            if len(self.immediate_args) != len(self.opcode.immediate_args):
                raise CompilerError('Invalid number of immediate args', token=self.token)
            
            for i, arg in enumerate(self.immediate_args):
                spec = self.opcode.immediate_args[i]
                if spec.reference:
                    field = langspec.fields[self.command]
                    if not arg in field.enums:
                        enum_names = [enum.name for enum in field.enums]
                        raise CompilerError(
                            'Invalid immediate arg type, One of enums({}) expected'.format(enum_names),
                            token=self.token
                        )

class Label(Node):

    def emit(self):
        lines = super().emit()
        lines.insert(0, lines.pop())
        return lines

class Comment(Node):

    def emit(self):
        return ['//{}'.format(line) for line in self.token.value.split('\n')]
