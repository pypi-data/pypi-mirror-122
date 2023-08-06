from error import Error

class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.advance()

    def raise_error(self):
        raise Error('Syntax error')

    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self):
        if self.current_token[0] == 'eof':
            return ('empty',)

        result = self.statements()

        if self.current_token[0] != 'eof':
            self.raise_error()

        return result

    def statements(self):
        statements = []

        statement = self.expr()
        statements.append(statement)

        while self.current_token[0] != 'eof' and self.current_token[0] == 'newline':
            self.advance()
            statements.append(self.expr())

        return ('statements', *statements)

    def expr(self):
        if self.current_token[0] == 'lcurly':
            return self.func_expr()

        return self.assignment_expr()

    def func_expr(self):
        self.advance()

        if self.current_token[0] == 'rcurly':
            self.advance()
            return ('func', ('empty',))

        body = self.statements()

        if self.current_token[0] != 'rcurly':
            self.raise_error()

        self.advance()
        return ('func', body)

    def assignment_expr(self):
        result = self.ternary_expr()

        while self.current_token[0] != 'eof' and self.current_token[0] == 'eq':
            self.advance()
            result = ('assign', result, self.expr())

        return result

    def ternary_expr(self):
        result = self.xor_expr()
        
        if self.current_token[0] == 'question':
            self.advance()

            if_expr = self.expr()
            
            if self.current_token[0] != 'colon':
                self.raise_error()

            self.advance()
            else_expr = self.expr()

            return ('ternary', result, if_expr, else_expr)
        
        return result

    def xor_expr(self):
        result = self.or_expr()

        while self.current_token[0] != 'eof' and self.current_token[0] == 'xor':
            self.advance()
            result = ('xor', result, self.or_expr())

        return result

    def or_expr(self):
        result = self.and_expr()

        while self.current_token[0] != 'eof' and self.current_token[0] == 'or':
            self.advance()
            result = ('or', result, self.and_expr())

        return result

    def and_expr(self):
        result = self.relational_expr()

        while self.current_token[0] != 'eof' and self.current_token[0] == 'and':
            self.advance()
            result = ('and', result, self.relational_expr())

        return result

    def relational_expr(self):
        result = self.equality_expr()

        while self.current_token[0] != 'eof' and self.current_token[0] in ('lt', 'gt', 'le', 'ge'):
            if self.current_token[0] == 'lt':
                self.advance()
                result = ('lt', result, self.equality_expr())
            elif self.current_token[0] == 'gt':
                self.advance()
                result = ('gt', result, self.equality_expr())
            elif self.current_token[0] == 'le':
                self.advance()
                result = ('le', result, self.equality_expr())
            elif self.current_token[0] == 'ge':
                self.advance()
                result = ('ge', result, self.equality_expr())

        return result

    def equality_expr(self):
        result = self.additive_expr()

        while self.current_token[0] != 'eof' and self.current_token[0] in ('ee', 'ne'):
            if self.current_token[0] == 'ee':
                self.advance()
                result = ('ee', result, self.additive_expr())
            elif self.current_token[0] == 'ne':
                self.advance()
                result = ('ne', result, self.additive_expr())

        return result

    def additive_expr(self):
        result = self.term()

        while self.current_token[0] != 'eof' and self.current_token[0] in ('plus', 'minus'):
            if self.current_token[0] == 'plus':
                self.advance()
                result = ('add', result, self.term())
            elif self.current_token[0] == 'minus':
                self.advance()
                result = ('subtract', result, self.term())

        return result

    def term(self):
        result = self.call_expr()

        while self.current_token[0] != 'eof' and self.current_token[0] in ('multiply', 'divide', 'mod'):
            if self.current_token[0] == 'multiply':
                self.advance()
                result = ('multiply', result, self.call_expr())
            elif self.current_token[0] == 'divide':
                self.advance()
                result = ('divide', result, self.call_expr())
            elif self.current_token[0] == 'mod':
                self.advance()
                result = ('mod', result, self.call_expr())
                
        return result

    def call_expr(self):
        factor = self.factor()

        while self.current_token[0] == 'lparen':
            self.advance()

            arg_nodes = []

            if self.current_token[0] == 'rparen':
                self.advance()
                return ('call', factor, ())
            else:
                arg_nodes.append(self.expr())

                while self.current_token[0] == 'comma':
                    self.advance()
                    arg_nodes.append(self.expr())

                self.advance()

                factor = ('call', factor, arg_nodes)
            
        return factor
                    
    def factor(self):
        token = self.current_token

        if token[0] == 'lparen':
            self.advance()
            result = self.expr()

            if self.current_token[0] != 'rparen':
                self.raise_error()
            
            self.advance()
            return result

        elif token[0] == 'number':
            self.advance()
            return ('number', token[1])

        elif token[0] == 'string':
            self.advance()
            return ('string', token[1])

        elif token[0] == 'pound':
            self.advance()
            return ('pound',)

        elif token[0] == 'name':
            self.advance()
            return ('name', token[1])

        elif token[0] == 'plus':
            self.advance()
            return ('plus', self.factor())
        
        elif token[0] == 'minus':
            self.advance()
            return ('minus', self.factor())

        elif token[0] == 'not':
            self.advance()
            return ('not', self.factor())

        elif token[0] == 'invert':
            self.advance()
            return ('invert', self.factor())

        self.raise_error()