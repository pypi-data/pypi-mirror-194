import json
from komandr import *
from dataclasses import asdict
from steal.scanner import scan
from steal.ast import Node
from steal import langspec 

@command
def compile(filename):
    with open(filename) as f:
        tokens = scan(f)
        while True:
            try:
                print(Node.from_tokens(tokens))
            except StopIteration:
                break

@command
def spec(opcode):
    try:
        print(json.dumps(asdict(langspec.opcodes[opcode]), indent=4))
    except KeyError:
        print('Opcode not found')