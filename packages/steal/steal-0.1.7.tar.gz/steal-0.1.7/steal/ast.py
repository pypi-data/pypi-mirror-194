import sys

from io import IOBase, StringIO
from typing import TypeVar, Generic, List, Generator, Optional
from dataclasses import dataclass, field

from steal import langspec
from steal.scanner import TokenType, Token, ASSIGNMENT

max_scratch_space = 256
scratch_space: List[str] = []

def new_assignment(token):
    name = token.value.rstrip(ASSIGNMENT)
    index = len(scratch_space)
    if index >= max_scratch_space:
        raise CompilerError('Scratch space overflow', token=token)
    scratch_space.append(name)
    return name, index

class CompilerError(Exception):
    
    def __init__(self, msg, token):
        super().__init__(msg)
        self.token = token

T = TypeVar('T')
@dataclass
class Node(Generic[T]):

    token: Token
    children: List = field(default_factory=lambda: [])

    def __post_init__(self):
        self.validate()

    def validate(self):
        pass

    @classmethod
    def from_tokens(cls, tokens: Generator[Token, None, None]) -> T:
        try:
            return cls._from_tokens(tokens)
        except CompilerError as e:
            print('Compiler error: {}'.format(str(e)), file=sys.stderr)
            print('Loc: {}, Line: {}, Token: {}'.format(
                e.token.location, e.token.line, e.token.value
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

        elif token.token_type == TokenType.BYTE:
            return Byte(token)
        elif token.token_type == TokenType.INT:
            return Int(token)
        elif token.token_type == TokenType.ATOM:
            name = token.value.split('.')[0]
            if name in langspec.opcodes:
                opcode = langspec.opcodes[name]
                return Opcode(token,
                              children=children,
                              opcode=opcode)
            elif name in scratch_space:
                return Ref(token)
            else:
                return Node(token=token, children=children)
        elif token.token_type == TokenType.LABEL:
            return Label(token, children=children)
        elif token.token_type == TokenType.ASSIGNMENT:
            return Assignment(token, children=children)
        elif token.token_type == TokenType.COMMENT:
            return Comment(token, children=children)

        raise CompilerError('Invalid token', token=token)
    
    @property
    def signature(self):
        return self.token.value.split('.')

    @property
    def name(self):
        return self.signature[0]

    @property
    def immediate_args(self):
        if len(self.signature) > 1:
            return self.signature[1:]
        return []

    def statement(self):
        return ' '.join(self.token.value.split('.'))

    def emit(self):
        lines = []
        if self.children:
            for child in self.children:
                lines.extend(child.emit())
        lines.append(self.statement())
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

    def validate(self):

        if self.children:
            non_comments =\
                [c for c in self.children if c.token.token_type != TokenType.COMMENT]
            if self.opcode.args and len(non_comments) != len(self.opcode.args):
                raise CompilerError('Invalid stack args', token=self.token)

        if self.opcode.immediate_args:
            if len(self.immediate_args) != len(self.opcode.immediate_args):
                raise CompilerError('Invalid immediate args', token=self.token)

class Int(Node):

    def statement(self):
        return 'pushint {}'.format(self.token.value)

class Byte(Node):

    def statement(self):
        return 'pushbytes "{}"'.format(self.token.value)

class Label(Node):

    def emit(self):
        lines = super().emit()
        lines.insert(0, lines.pop())
        return lines

@dataclass
class Assignment(Node):

    def statement(self):
        name, index = new_assignment(self.token)
        return 'store {} // {}'.format(index, name)

class Ref(Node):

    def emit(self):
        index = scratch_space.index(self.token.value)
        return ['load {} // {}'.format(index, self.token.value)]

class Comment(Node):

    def emit(self):
        return ['//{}'.format(line) for line in self.token.value.split('\n')]
