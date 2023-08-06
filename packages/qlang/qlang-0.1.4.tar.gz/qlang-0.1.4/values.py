import math

from error import Error
from dataclasses import dataclass

class Value:    
    def add(self, other):
        self.illegal_operation()

    def subtract(self, other):
        self.illegal_operation()

    def multiply(self, other):
        self.illegal_operation()

    def divide(self, other):
        self.illegal_operation()

    def mod(self, other):
        self.illegal_operation()

    def eq(self, other):
        self.illegal_operation()

    def ne(self, other):
        self.illegal_operation()

    def lt(self, other):
        self.illegal_operation()

    def gt(self, other):
        self.illegal_operation()

    def le(self, other):
        self.illegal_operation()

    def ge(self, other):
        self.illegal_operation()

    def and_(self, other):
        self.illegal_operation()

    def or_(self, other):
        self.illegal_operation()

    def xor(self, other):
        self.illegal_operation()

    def plus(self):
        self.illegal_operation()        

    def minus(self):
        self.illegal_operation()

    def not_(self):
        self.illegal_operation()

    def invert(self):
        self.illegal_operation()

    def pound(self):
        self.illegal_operation()

    def illegal_operation(self):
        raise Error('Illegal operation')
    
    def __repr__(self):
        return f'{self.value}'

@dataclass
class Number(Value):
    value: float
    
    def add(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)
        else:
            self.illegal_operation()

    def subtract(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)
        else:
            self.illegal_operation()

    def multiply(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)
        else:
            self.illegal_operation()

    def divide(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)
        else:
            self.illegal_operation()

    def mod(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value)
        else:
            self.illegal_operation()

    def eq(self, other):
        if isinstance(other, Number):
            return Number(float(self.value == other.value))
        else:
            return Number(0.0)

    def ne(self, other):
        if isinstance(other, Number):
            return Number(float(self.value != other.value))
        else:
            return Number(1.0)

    def lt(self, other):
        if isinstance(other, Number):
            return Number(float(self.value < other.value))
        else:
            return self.illegal_operation()

    def gt(self, other):
        if isinstance(other, Number):
            return Number(float(self.value > other.value))
        else:
            return self.illegal_operation()

    def le(self, other):
        if isinstance(other, Number):
            return Number(float(self.value <= other.value))
        else:
            return self.illegal_operation()

    def ge(self, other):
        if isinstance(other, Number):
            return Number(float(self.value >= other.value))
        else:
            return self.illegal_operation()

    def and_(self, other):
        if isinstance(other, Number):
            return Number(float(bool(self.value) and bool(other.value)))
        else:
            return self.illegal_operation()

    def or_(self, other):
        if isinstance(other, Number):
            return Number(float(bool(self.value) or bool(other.value)))
        else:
            return self.illegal_operation()

    def xor(self, other):
        if isinstance(other, Number):
            return Number(float(bool(self.value) != bool(other.value)))
        else:
            return self.illegal_operation()

    def plus(self):
        return Number(+self.value)

    def minus(self):
        return Number(-self.value)    

    def not_(self):
        return Number(float(not bool(self.value)))

    def invert(self):
        return Number(float(~math.floor(self.value)))

    def __repr__(self):
        return f'{self.value}'

@dataclass
class String(Value):
    value: str
    
    def add(self, other):
        if isinstance(other, String):
            return String(self.value + other.value)
        else:
            self.illegal_operation()

    def eq(self, other):
        if isinstance(other, String):
            return Number(float(self.value == other.value))
        else:
            return Number(0.0)

    def ne(self, other):
        if isinstance(other, String):
            return Number(float(self.value != other.value))
        else:
            return Number(1.0)  
                 
    def pound(self):
        return Number(float(len(self.value)))

    def __repr__(self):
        return f'{self.value}'
           
@dataclass
class At(Value):
    def eq(self, other):
        return Number(float(isinstance(other, At)))

    def ne(self, other):
        return Number(float(not isinstance(other, At)))

    def __repr__(self):
        return '@'
        
@dataclass
class Func(Value):
    func: any

    def __repr__(self):
        return '<function>'