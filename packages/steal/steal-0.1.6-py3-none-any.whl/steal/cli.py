from komandr import *

from steal.scanner import scan
from steal.ast import Node

@command
def compile(filename):
    with open(filename) as f:
        tokens = scan(f)
        while True:
            try:
                print(Node.from_tokens(tokens))
            except StopIteration:
                break
