import sys
import json
from dataclasses import asdict

from komandr import command, arg, main as komandr_main

from steal.config import Config
from steal.ast import Node, CompilerError
from steal import langspec


@command
@arg('file', help='file to read')
@arg('strict', '-s', help="strict mode", action='store_true')
def compile(path, strict=False):
    with open(path, encoding='utf-8') as f:
        try:
            print(Node.from_file(f, config=Config(strict=strict)))
        except CompilerError as e:
            print('Compiler error: {}'.format(str(e)), file=sys.stderr)
            if e.token:
                print('Ln: {}, Col: {}, Token: {}'.format(
                    e.token.line, e.token.col, e.token.value
                ), file=sys.stderr)
            exit(1)


@command
def spec(opcode: str):
    try:
        print(json.dumps(asdict(langspec.opcodes[opcode]), indent=4))
    except KeyError:
        print('Opcode not found', file=sys.stderr)
        exit(1)


def main(*args, **kwargs):
    komandr_main(*args, **kwargs)
