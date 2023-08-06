from io import IOBase, StringIO
from typing import TypeVar, Generic, List, Generator, Optional
from dataclasses import dataclass

from steal import langspec
from steal.config import Config
from steal.scanner import TokenType, Token, scan

max_scratch_space = 256
scratch_space: List[str] = []


def allocate_scratch_space(name: str) -> int:
    index = len(scratch_space)
    if index < max_scratch_space:
        scratch_space.append(name)
        return index
    return -1


def refer_scratch_space(name) -> int:
    try:
        return scratch_space.index(name)
    except ValueError:
        return -1


class CompilerError(Exception):

    def __init__(self, msg, token: Token = None):
        super().__init__(msg)
        self.token = token


T = TypeVar('T')


@dataclass
class Node(Generic[T]):

    token: Token
    children: Optional[List[T]] = None
    immediate_args_override: Optional[List[str]] = None
    note: str = None
    config: Optional[Config] = None

    def __post_init__(self):
        self.validate()

    def validate(self):
        pass

    @classmethod
    def from_str(cls, input, config: Optional[Config] = None):
        return Node.from_tokens(scan(StringIO(input)), config=config)

    @classmethod
    def from_file(cls, file, config: Optional[Config] = None):
        return Node.from_tokens(scan(file), config=config)

    @classmethod
    def from_tokens(cls, tokens: Generator[Token, None, None],
                    config: Config = None) -> T:

        config = config or Config()
        children = []
        while True:
            try:
                child = Node._from_tokens(tokens, config=config)
                children.append(child)
            except StopIteration:
                break
        return Node(None, children=children, config=config)

    @classmethod
    def _from_tokens(cls, tokens: Generator[Token, None, None],
                     head: Optional[Token] = None,
                     children: Optional[List[T]] = None,
                     config: Optional[Config] = None) -> T:

        token = head or next(tokens)

        if token.token_type == TokenType.BEGIN:
            head = next(tokens)
            token = next(tokens)
            children = []

            while token.token_type != TokenType.END:
                child = Node._from_tokens(tokens, head=token, config=config)
                children.append(child)
                token = next(tokens)

            if token.token_type != TokenType.END:
                raise CompilerError('Unclosed expression', token=token)

            return Node._from_tokens(tokens,
                                     head=head,
                                     children=children,
                                     config=config)

        elif token.token_type == TokenType.ATOM:
            if token.head in langspec.opcodes:
                spec = langspec.opcodes[token.head]
                return Opcode(token,
                              children=children,
                              spec=spec,
                              config=config)
            raise CompilerError('Invalid opcode', token=token)
        elif token.token_type == TokenType.VARIABLE:
            if children:
                index = allocate_scratch_space(token.value)
                if index < 0:
                    raise CompilerError('Scratch space overflow', token=token)
                return Opcode(token,
                              spec=langspec.opcodes['store'],
                              immediate_args_override=[str(index)],
                              children=children,
                              note=token.value,
                              config=config)
            else:
                index = refer_scratch_space(token.value)
                if index < 0:
                    raise CompilerError('Scratch space not found', token=token)

                return Opcode(token,
                              spec=langspec.opcodes['load'],
                              children=children,
                              immediate_args_override=[str(index)],
                              note=token.value,
                              config=config)
        elif token.token_type == TokenType.BYTE:
            return Opcode(token,
                          spec=langspec.opcodes['byte'],
                          children=children,
                          immediate_args_override=[token.value],
                          config=config)
        elif token.token_type == TokenType.INT:
            return Opcode(token,
                          spec=langspec.opcodes['int'],
                          children=children,
                          immediate_args_override=[token.value],
                          config=config)
        elif token.token_type == TokenType.LABEL:
            return Label(token, children=children, config=config)
        elif token.token_type == TokenType.COMMENT:
            return Comment(token, children=children, config=config)
        elif token.token_type == TokenType.PRAGMA:
            return Pragma(token, children=children, config=config)

        raise CompilerError('Invalid token', token=token)

    @property
    def stack_height(self):
        return sum([child.stack_height for child in self.children or []])

    @property
    def command(self) -> str:
        return self.token.head

    @property
    def immediate_args(self) -> List[str]:
        return self.immediate_args_override or self.token.rest

    @property
    def statement(self) -> str:
        return ' '.join([self.command, *self.immediate_args])

    def emit(self) -> List[str]:
        lines = []
        if self.children:
            for child in self.children:
                lines.extend(child.emit())
        if self.token:
            if self.note:
                lines.append('{} // {}'.format(self.statement, self.note))
            else:
                lines.append('{}'.format(self.statement))
        return lines

    def write(self, f: IOBase):
        f.writelines(['{}\n'.format(line) for line in self.emit()])

    def __str__(self) -> str:
        with StringIO() as io:
            self.write(io)
            return io.getvalue()


@dataclass
class Opcode(Node):

    spec: langspec.Opcode = None

    @property
    def noncomments(self):
        if self.children:
            return filter(lambda c: c.token.token_type != TokenType.COMMENT,
                          self.children)
        return []

    @property
    def statement(self):
        return ' '.join([self.spec.name, *self.immediate_args])

    @property
    def children_height(self):
        return sum([len(c.spec.returns or []) for c in self.noncomments])

    @property
    def return_height(self):
        return len(self.spec.returns or [])

    @property
    def arg_height(self):
        return len(self.spec.args or [])

    @property
    def stack_height(self):
        return self.return_height - (self.arg_height - self.children_height)

    def validate(self):

        super().validate()

        if self.spec.args:
            if self.config.strict and self.arg_height != self.children_height:
                raise CompilerError('Invalid number of stack args',
                                    token=self.token)

        if self.config.strict and self.spec.immediate_args:
            if len(self.immediate_args) != len(self.spec.immediate_args):
                raise CompilerError('Invalid number of immediate args',
                                    token=self.token)

            for i, arg in enumerate(self.immediate_args):
                spec = self.spec.immediate_args[i]
                if spec.reference:
                    field = langspec.fields[self.command]
                    if arg not in field.enums:
                        enum_names = ', '.join([enum for enum in field.enums])
                        raise CompilerError(
                            'Invalid arg, need one of {})'.format(enum_names),
                            token=self.token
                        )
                else:
                    # Validate non-ref immediate args
                    pass


class Label(Node):

    def emit(self):
        lines = super().emit()
        lines.insert(0, lines.pop())
        return lines


class Comment(Node):

    def emit(self):
        return ['//{}'.format(line) for line in self.token.value.split('\n')]


class Pragma(Node):
    pass
