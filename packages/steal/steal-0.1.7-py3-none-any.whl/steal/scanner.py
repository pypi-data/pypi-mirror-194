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
    line: int
    location: int

    def __repr__(self):
        return '{}({})'.format(self.token_type.name, self.value)
    

def scan(f: TextIO) -> Generator[Token, None, None]:

    line = 1
    location = 0

    def consume_one():
        nonlocal line, location
        c = f.read(1)
        if c == NEWLINE:
            line += 1
        location += 1
        return c

    def consume(unless: Callable, c: str):
        value = ''
        while unless(c):
            value += c
            c = consume_one()
        return c, value

    def atom_test(c):
        return c not in TERMINALS and not c.isspace()

    def token(*args, **kwargs):
        kwargs['line'] = line
        kwargs['location'] = location
        return Token(*args, **kwargs)

    c = consume_one()
    while c:
        if c == LEFT_PAREN:
            yield token(TokenType.BEGIN, LEFT_PAREN)
            c = consume_one()
        elif c == RIGHT_PAREN:
            yield token(TokenType.END, RIGHT_PAREN)
            c = consume_one()
        elif c == COMMENT:
            c, value = consume(lambda c: c != COMMENT, consume_one())
            yield token(TokenType.COMMENT, value)
            c = consume_one()
        elif c == STRING_DELIMETER:
            c, value = consume(lambda c: c != STRING_DELIMETER, consume_one())
            yield token(TokenType.BYTE, value)
            c = consume_one()
        elif c.isnumeric():
            c, value = consume(lambda c: c.isnumeric(), c)
            yield token(TokenType.INT, value)
        elif atom_test(c):
            c, value = consume(atom_test, c)
            if value.endswith(LABEL_COLON):
                yield token(TokenType.LABEL, value)
            elif value.endswith(ASSIGNMENT):
                yield token(TokenType.ASSIGNMENT, value)
            else:
                yield token(TokenType.ATOM, value)
        else:
            c = consume_one()

def main():
    with open(sys.argv[1]) as f:
        for token in scan(f):
            print(token)

if __name__ == '__main__':
    main()