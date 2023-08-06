import math

from error import Error
from values import *
from symbol_table import SymbolTable

class Interpreter:
    def visit(self, node, symbol_table):
        if node[0] == 'empty':
            return self.visit_empty_node(node, symbol_table)
        elif node[0] == 'number':
            return self.visit_number_node(node, symbol_table)
        elif node[0] == 'string':
            return self.visit_string_node(node, symbol_table)
        elif node[0] == 'at':
            return self.visit_at_node(node, symbol_table)
        elif node[0] == 'name':
            return self.visit_name_node(node, symbol_table)    
        elif node[0] == 'add':
            return self.visit_add_node(node, symbol_table)
        elif node[0] == 'subtract':
            return self.visit_subtract_node(node, symbol_table)
        elif node[0] == 'multiply':
            return self.visit_multiply_node(node, symbol_table)
        elif node[0] == 'divide':
            return self.visit_divide_node(node, symbol_table)
        elif node[0] == 'mod':
            return self.visit_mod_node(node, symbol_table)
        elif node[0] == 'ee':
            return self.visit_ee_node(node, symbol_table) 
        elif node[0] == 'ne':
            return self.visit_ne_node(node, symbol_table)   
        elif node[0] == 'lt':
            return self.visit_lt_node(node, symbol_table)   
        elif node[0] == 'le':
            return self.visit_le_node(node, symbol_table)   
        elif node[0] == 'gt':
            return self.visit_gt_node(node, symbol_table)    
        elif node[0] == 'ge':
            return self.visit_ge_node(node, symbol_table)    
        elif node[0] == 'and':
            return self.visit_and_node(node, symbol_table)   
        elif node[0] == 'or':
            return self.visit_or_node(node, symbol_table)   
        elif node[0] == 'xor':
            return self.visit_xor_node(node, symbol_table)    
        elif node[0] == 'plus':
            return self.visit_plus_node(node, symbol_table)
        elif node[0] == 'minus':
            return self.visit_minus_node(node, symbol_table)
        elif node[0] == 'not':
            return self.visit_not_node(node, symbol_table)
        elif node[0] == 'invert':
            return self.visit_invert_node(node, symbol_table)
        elif node[0] == 'pound':
            return self.visit_pound_node(node, symbol_table)
        elif node[0] == 'assign':
            return self.visit_assign_node(node, symbol_table)    
        elif node[0] == 'ternary':
            return self.visit_ternary_node(node, symbol_table)    
        elif node[0] == 'func':
            return self.visit_func_node(node, symbol_table)
        elif node[0] == 'call':
            return self.visit_call_node(node, symbol_table)
        elif node[0] == 'statements':
            return self.visit_statements_node(node, symbol_table)
        else:
            raise Exception(f'Unknown node type')

    def visit_empty_node(self, node, symbol_table):
        return At()

    def visit_number_node(self, node, symbol_table):
        return Number(node[1])

    def visit_string_node(self, node, symbol_table):
        return String(node[1])

    def visit_at_node(self, node, symbol_table):
        return At()

    def visit_name_node(self, node, symbol_table):
        name = node[1]

        result = symbol_table.get(name)

        if result is None:
            raise Error(f'{name} is not defined')
        
        return result

    def visit_add_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).add(self.visit(node[2], symbol_table))
    
    def visit_subtract_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).subtract(self.visit(node[2], symbol_table))

    def visit_multiply_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).multiply(self.visit(node[2], symbol_table))

    def visit_divide_node(self, node, symbol_table):
        try:
            return self.visit(node[1], symbol_table).divide(self.visit(node[2], symbol_table))
        except ZeroDivisionError:
            return Number(math.inf)

    def visit_mod_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).mod(self.visit(node[2], symbol_table))

    def visit_ee_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).eq(self.visit(node[2], symbol_table))

    def visit_ne_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).ne(self.visit(node[2], symbol_table))

    def visit_lt_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).lt(self.visit(node[2], symbol_table))

    def visit_gt_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).gt(self.visit(node[2], symbol_table))

    def visit_le_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).le(self.visit(node[2], symbol_table))

    def visit_ge_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).ge(self.visit(node[2], symbol_table))

    def visit_and_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).and_(self.visit(node[2], symbol_table))

    def visit_or_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).or_(self.visit(node[2], symbol_table))

    def visit_xor_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).xor_(self.visit(node[2], symbol_table))
        
    def visit_plus_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).plus()

    def visit_minus_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).minus()

    def visit_not_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).not_()

    def visit_invert_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).invert()

    def visit_pound_node(self, node, symbol_table):
        return self.visit(node[1], symbol_table).pound()

    def visit_assign_node(self, node, symbol_table):
        if node[1][0] != 'name':
            raise Error('Invalid left-hand side in assignment')

        name = node[1][1]
        value = self.visit(node[2], symbol_table)

        symbol_table.set(name, value)
    
        return value

    def visit_ternary_node(self, node, symbol_table):
        condition = self.visit(node[1], symbol_table)

        if not isinstance(condition, Number):
            raise Error(f'{condition} is not a number')
    
        if condition.value:
            return self.visit(node[2], symbol_table)
        else:
            return self.visit(node[3], symbol_table)

    def visit_func_node(self, node, symbol_table):
        def func(args):
            new_symbol_table = SymbolTable(symbol_table)

            for i in range(0, len(args)):
                new_symbol_table.set(f'${i}', args[i])
            
            return self.visit(node[1], new_symbol_table)
            
        return Func(func)

    def visit_call_node(self, node, symbol_table):
        func = self.visit(node[1], symbol_table)
        args = []

        for arg_node in node[2]:
            args.append(self.visit(arg_node, symbol_table))

        return func.func(args)

    def visit_statements_node(self, node, symbol_table):
        for i in range(1, len(node) - 1):
            self.visit(node[i], symbol_table)

        return self.visit(node[-1], symbol_table)
 