import string

from error import Error

WHITESPACE = ' \t'
LETTERS = string.ascii_letters + '_$'
DIGITS = '0123456789'

class Lexer:
    def __init__(self, text):
        self.text = iter(text)
        self.advance()
    
    def advance(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None
    
    def get_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in WHITESPACE:
                self.advance()
            elif self.current_char == ';' or self.current_char == '\n':
                self.advance()
                tokens.append(('newline',))
            elif self.current_char == '.' or self.current_char in DIGITS:
                tokens.append(self.get_number())
            elif self.current_char in LETTERS:
                tokens.append(self.get_name())
            elif self.current_char == '"':
                tokens.append(self.get_string())
            elif self.current_char == '+':
                self.advance()
                tokens.append(('plus',))
            elif self.current_char == '-':
                self.advance()
                tokens.append(('minus',))
            elif self.current_char == '*':
                self.advance()
                tokens.append(('multiply',))
            elif self.current_char == '/':
                self.advance()
                tokens.append(('divide',))
            elif self.current_char == '%':
                self.advance()
                tokens.append(('mod',))
            elif self.current_char == '<':
                tokens.append(self.get_lt())
            elif self.current_char == '=':
                tokens.append(self.get_eq())
            elif self.current_char == '>':
                tokens.append(self.get_gt())
            elif self.current_char == '&':
                self.advance()
                tokens.append(('and',))
            elif self.current_char == '|':
                self.advance()
                tokens.append(('or',)) 
            elif self.current_char == '^':
                self.advance()
                tokens.append(('xor',))
            elif self.current_char == '!':
                tokens.append(self.get_not())  
            elif self.current_char == '~':
                self.advance()
                tokens.append(('invert',))
            elif self.current_char == '?':
                self.advance()
                tokens.append(('question',))     
            elif self.current_char == ':':
                self.advance()
                tokens.append(('colon',))  
            elif self.current_char == ',':
                self.advance()
                tokens.append(('comma',))  
            elif self.current_char == '#':
                self.advance()
                tokens.append(('pound',))                              
            elif self.current_char == '(':
                self.advance()
                tokens.append(('lparen',))
            elif self.current_char == ')':
                self.advance()
                tokens.append(('rparen',))
            elif self.current_char == '{':
                self.advance()
                tokens.append(('lcurly',)) 
            elif self.current_char == '}':
                self.advance()
                tokens.append(('rcurly',)) 
            else:
                raise Error('Lexical error')

        tokens.append(('eof',))

        return tokens

    def get_number(self):
        decimal_point_count = 0
        number_str = self.current_char
        self.advance()

        while self.current_char != None and (self.current_char == '.' or self.current_char in DIGITS):
            if self.current_char == '.':
                decimal_point_count += 1
                if decimal_point_count > 1:
                    break
            
            number_str += self.current_char
            self.advance()

        if number_str.startswith('.'):
            number_str = '0' + number_str
        if number_str.endswith('.'):
            number_str += '0'

        return ('number', float(number_str))

    def get_name(self):
        name_str = self.current_char
        self.advance()

        while self.current_char != None and (self.current_char in LETTERS or self.current_char in DIGITS):
            name_str += self.current_char
            self.advance()

        return ('name', name_str)
    
    def get_string(self):   
        string = ''
        escape_character = False
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        while self.current_char != None and (self.current_char != '"' or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
                    escape_character = False
                    
            self.advance()
        
        self.advance()
        
        return ('string', string)

    def get_lt(self):
        self.advance()
        if self.current_char == '=':
            self.advance()
            return ('le',)
        else:
            return ('lt',)

    def get_eq(self):
        self.advance()
        if self.current_char == '=':
            self.advance()
            return ('ee',)
        else:
            return ('eq',)

    def get_gt(self):
        self.advance()
        if self.current_char == '=':
            self.advance()
            return ('ge',)
        else:
            return ('gt',)

    def get_not(self):
        self.advance()
        if self.current_char == '=':
            self.advance()
            return ('ne',)
        else:
            return ('not',)
