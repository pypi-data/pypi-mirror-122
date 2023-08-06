from symbol_table import SymbolTable
from values import *

def func_I(args):
    return String(input())

# def func_N(args):
#     return Number(float(args[0]))

def func_S(args):
    return String(str(args[0]))

def func_P(args):
    print(args[0])
    return At()

stdlib = SymbolTable()
stdlib.set('I', Func(func_I))
stdlib.set('S', Func(func_S))
# stdlib.set('N', Func(func_N))
stdlib.set('P', Func(func_P))