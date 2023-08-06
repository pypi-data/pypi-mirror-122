import math
import string
from lexer import Lexer
from parser_ import Parser
from interpreter import Interpreter
from symbol_table import SymbolTable
from stdlib import stdlib

def run(file):
    f = open(file, 'r')
    text = f.read()

    run_text(text)

def run_text(text):
    lexer = Lexer(text)
    tokens = lexer.get_tokens()

    parser = Parser(tokens)
    tree = parser.parse()

    interpreter = Interpreter()
    return interpreter.visit(tree, SymbolTable(stdlib))