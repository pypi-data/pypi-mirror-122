import math

from error import Error
from dataclasses import dataclass

class Value:
    value: float
    
    def __add__(self, other):
        self.illegal_operation()

    def __sub__(self, other):
        self.illegal_operation()

    def __mul__(self, other):
        self.illegal_operation()

    def __truediv__(self, other):
        self.illegal_operation()

    def __mod__(self, other):
        self.illegal_operation()

    def __eq__(self, other):
        self.illegal_operation()

    def __ne__(self, other):
        self.illegal_operation()

    def __lt__(self, other):
        self.illegal_operation()

    def __gt__(self, other):
        self.illegal_operation()

    def __le__(self, other):
        self.illegal_operation()

    def __ge__(self, other):
        self.illegal_operation()

    def __and__(self, other):
        self.illegal_operation()

    def __or__(self, other):
        self.illegal_operation()

    def __xor__(self, other):
        self.illegal_operation()

    def __not__(self):
        self.illegal_operation()

    def __invert__(self):
        self.illegal_operation()

    def __pos__(self):
        self.illegal_operation()        

    def __neg__(self):
        self.illegal_operation()

    def illegal_operation(self):
        raise Error('Illegal operation')
    
    def __repr__(self):
        return f'{self.value}'

@dataclass
class Number(Value):
    value: float
    
    def __add__(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)
        else:
            self.illegal_operation()

    def __sub__(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)
        else:
            self.illegal_operation()

    def __mul__(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)
        else:
            self.illegal_operation()

    def __truediv__(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)
        else:
            self.illegal_operation()

    def __mod__(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value)
        else:
            self.illegal_operation()

    def __eq__(self, other):
        if isinstance(other, Number):
            return Number(float(self.value == other.value))
        else:
            return Number(0.0)

    def __ne__(self, other):
        if isinstance(other, Number):
            return Number(float(self.value != other.value))
        else:
            return Number(1.0)

    def __lt__(self, other):
        if isinstance(other, Number):
            return Number(float(self.value < other.value))
        else:
            return self.illegal_operation()

    def __gt__(self, other):
        if isinstance(other, Number):
            return Number(float(self.value > other.value))
        else:
            return self.illegal_operation()

    def __le__(self, other):
        if isinstance(other, Number):
            return Number(float(self.value <= other.value))
        else:
            return self.illegal_operation()

    def __ge__(self, other):
        if isinstance(other, Number):
            return Number(float(self.value >= other.value))
        else:
            return self.illegal_operation()

    def __and__(self, other):
        if isinstance(other, Number):
            return Number(float(bool(self.value) and bool(other.value)))
        else:
            return self.illegal_operation()

    def __or__(self, other):
        if isinstance(other, Number):
            return Number(float(bool(self.value) or bool(other.value)))
        else:
            return self.illegal_operation()

    def __xor__(self, other):
        if isinstance(other, Number):
            return Number(float(bool(self.value) != bool(other.value)))
        else:
            return self.illegal_operation()

    def not_(self):
        return Number(float(not bool(self.value)))

    def __invert__(self):
        return Number(float(~math.floor(self.value)))

    def __pos__(self):
        return Number(+self.value)

    def __neg__(self):
        return Number(-self.value)    

    def __repr__(self):
        return f'{self.value}'

@dataclass
class String(Value):
    value: str
    
    def __add__(self, other):
        if isinstance(other, String):
            return String(self.value + other.value)
        else:
            self.illegal_operation()

    def __eq__(self, other):
        if isinstance(other, String):
            return Number(float(self.value == other.value))
        else:
            return Number(0.0)

    def __ne__(self, other):
        if isinstance(other, String):
            return Number(float(self.value != other.value))
        else:
            return Number(1.0)        

    def __repr__(self):
        return f'{self.value}'
           
@dataclass
class Pound(Value):
    def __eq__(self, other):
        return Number(float(isinstance(other, Pound)))

    def __ne__(self, other):
        return Number(float(not isinstance(other, Pound)))

    def __repr__(self):
        return '#'

@dataclass
class Func(Value):
    func: any

    def __repr__(self):
        return '<function>'
    