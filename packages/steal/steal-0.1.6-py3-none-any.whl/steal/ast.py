from io import IOBase, StringIO
from typing import TypeVar, Generic, List, Generator
from dataclasses import dataclass, field
from steal.langspec import opcodes, Opcode
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
    
    def __init__(self, msg, **kwargs):
        self.token = kwargs.get('token')
        super().__init__('{} (Token = {})'.format(msg, self.token))

T = TypeVar('T')
@dataclass
class Node(Generic[T]):

    token: Token
    children: List = field(default_factory=lambda: [])

    def validate(self):
        pass

    @classmethod
    def from_tokens(cls, tokens: Generator[Token, None, None], head: Token = None) -> T:
        token = head or next(tokens)
        if token.token_type == TokenType.BEGIN:
            node = Node.from_tokens(tokens)
            token = next(tokens)
            while token.token_type != TokenType.END:
                child = Node.from_tokens(tokens, head=token)
                node.children.append(child)
                token = next(tokens)

            if token.token_type != TokenType.END:
                raise CompilerError('Unclosed expression', token=token)

            return node
        elif token.token_type == TokenType.BYTE:
            return Byte(token)
        elif token.token_type == TokenType.INT:
            return Int(token)
        elif token.token_type == TokenType.ATOM:
            if token.value in opcodes:
                return Opcode(token, opcode=opcodes[token.value])
            elif token.value in scratch_space:
                return Ref(token)
            else:
                # Or return compiler error?
                return Node(token=token)

        elif token.token_type == TokenType.LABEL:
            return Label(token)
        elif token.token_type == TokenType.ASSIGNMENT:
            return Assignment(token)
        elif token.token_type == TokenType.COMMENT:
            return Comment(token)

        raise CompilerError('Invalid token', token=token)

    def statement(self):
        return ' '.join(self.token.value.split('.'))

    def emit(self):
        lines = []
        for child in self.children:
            lines.extend(child.emit())
        lines.append(self.statement())
        return lines

    def write(self, f: IOBase):
        self.validate()
        f.writelines(['{}\n'.format(line) for line in self.emit()])

    def __str__(self) -> str:
        with StringIO() as io:
            self.write(io)
            return io.getvalue()
@dataclass
class Opcode(Node):

    opcode: Opcode = None

    def validate(self):

        if len(self.children) != len(self.opcode.arg_types):
            raise CompilerError('Invalid stack args', token=self.token)

        # TODO: Check for other semantic validations
        # if len(node.immediate_args) != opcode.size - 1:
        #     raise CompilerError('Invalid immediate args', token=token)

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
