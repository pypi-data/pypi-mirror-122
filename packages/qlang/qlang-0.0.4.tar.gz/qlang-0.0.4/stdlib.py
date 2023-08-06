from symbol_table import SymbolTable
from values import *

# def func_I(args):
#     input()
#     return Pound()

def func_P(args):
    print(args[0])
    return Pound()

stdlib = SymbolTable()
stdlib.set('P', Func(func_P))