import sys
from enum import Enum
from typing import TextIO, Generator
from collections.abc import Callable
from dataclasses import dataclass

STRING_DELIMETER = '"'
LABEL_COLON = ':'
LEFT_PAREN = '('
RIGHT_PAREN = ')'
ASSIGNMENT = '>'
COMMENT = '`'
NEWLINE = '\n'

TERMINALS = [LEFT_PAREN, RIGHT_PAREN, STRING_DELIMETER, NEWLINE]

TokenType = Enum('TokenType', [
    'BEGIN',
    'END',
    'BYTE',
    'INT',
    'ATOM',
    'LABEL',
    'ASSIGNMENT',
    'COMMENT'
])

@dataclass
class Token:
    token_type: TokenType
    value: str

    def __repr__(self):
        return '{}({})'.format(self.token_type.name, self.value)
    

def scan(f: TextIO) -> Generator[Token, None, None]:
    def consume(unless: Callable, c: str):
        value = ''
        while unless(c):
            value += c
            c = f.read(1)
        return c, value

    def atom_test(c):
        return c not in TERMINALS and not c.isspace()

    c = f.read(1)
    while c:
        if c == LEFT_PAREN:
            yield Token(TokenType.BEGIN, LEFT_PAREN)
            c = f.read(1)
        elif c == RIGHT_PAREN:
            yield Token(TokenType.END, RIGHT_PAREN)
            c = f.read(1)
        elif c == COMMENT:
            c, value = consume(lambda c: c != COMMENT, f.read(1))
            yield Token(TokenType.COMMENT, value)
            c = f.read(1)
        elif c == STRING_DELIMETER:
            c, value = consume(lambda c: c != STRING_DELIMETER, f.read(1))
            yield Token(TokenType.BYTE, value)
            c = f.read(1)
        elif c.isnumeric():
            c, value = consume(lambda c: c.isnumeric(), c)
            yield Token(TokenType.INT, value)
        elif atom_test(c):
            c, value = consume(atom_test, c)
            if value.endswith(LABEL_COLON):
                yield Token(TokenType.LABEL, value)
            elif value.endswith(ASSIGNMENT):
                yield Token(TokenType.ASSIGNMENT, value)
            else:
                yield Token(TokenType.ATOM, value)
        else:
            c = f.read(1)

def main():
    with open(sys.argv[1]) as f:
        for token in scan(f):
            print(token)

if __name__ == '__main__':
    main()