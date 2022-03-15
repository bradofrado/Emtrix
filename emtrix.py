from enum import Enum
import re
import numpy as np

from tokens import TokenType

class ObjectType(Enum):
    Matrix = 0
    Int = 1

class OperatorType(Enum):
    PLUS = lambda x, y: x + y,
    MINUS = lambda x, y: x - y,
    MULTIPLY = lambda x, y: x * y,
    DIVIDE = lambda x, y: x / y,
    DET = lambda x: x.det(),
    EIG = lambda x: x.eig(),
    INV = lambda x: x.inv(),

class Value():
    def __init__(self):
        self.value = None
        pass
    def __str__(self) -> str:
        return str(self.value)
    def __repr__(self) -> str:
        return self.__str__()
    def getValue(self):
        return self.value
    def __mul__(self, other):
        if isinstance(other, Value):
            return self.value * other.getValue()
        return self.value * other
    __rmul__ = __mul__
    def __truediv__(self, other):
        if isinstance(other, Value):
            return self.value / other.getValue()
        return self.value / other
    def __add__(self, other):
        if isinstance(other, Value):
            return self.value + other.getValue()
        return self.value + other
    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Value):
            return self.value - other.getValue()
        return self.value - other

    def eig(self):
        raise Exception("Cannot perform the operation eig on this data type")
    def det(self):
        raise Exception("Cannot perform the operation det on this data type")
    def inv(self):
        raise Exception("Cannot perform the operation inv on this data type")

class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = int(value)
    def getValue(self):
        return self.value
class Matrix(Value):
    def __init__(self, rows):
        super().__init__()
        self.value = np.array(rows, dtype=int)
    def getValue(self):
        return self.value
    def __mul__ (self, other):
        if isinstance(other, Matrix):
            return np.matmul(self.value, other.getValue())
        return super().__mul__(other)
    __rmul__ = __mul__
    def __add__(self, other):
        if isinstance(other, Matrix):
            return np.add(self.value, other.getValue())
        return super().__add__(other)
    def __sub__(self, other):
        if isinstance(other, Matrix):
            return np.subtract(self.value, other.getValue())
        return super().__sub__(other)
    __rsub__ = __sub__
    def __truediv__(self, other):
        #A/B can be seen as A*B^-1
        if isinstance(other, Matrix):
            return np.matmul(self.value, np.linalg.inv(other.getValue()))
        return super().__truediv__(other)
    def __rtruediv__(self, other):
        #A/B can be seen as A*B^-1
        if isinstance(other, Matrix):
            return np.matmul(self.value, np.linalg.inv(other.getValue()))
        return super().__truediv__(other)
    def eig(self):
        return np.linalg.eig(self.value)
    def det(self):
        return np.linalg.det(self.value)
    def inv(self):
        return np.linalg.inv(self.value)

class Function(Value):
    def __init__(self, value : Value, type : OperatorType):
        super().__init__()
        self.value = value
        self.type = type
    def getValue(self):
        return self.type.value[0](self.value)

class Computation(Value):
    def __init__(self, leftValue : Value, rightValue : Value, operator : OperatorType):
        super().__init__()
        self.leftValue = leftValue
        self.rightValue = rightValue
        self.operator = operator
    def getValue(self):
        return self.type.value[0](self.leftValue, self.rightValue)
        
    
class Variable(Value):
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value
        pass
    def getValue(self):
        return self.value.getValue()
    def __str__(self) -> str:
        return self.name + " = " + super().__str__()
    def __mul__(self, other):
        return 0

class Print():
    def __init__(self, _str : str, vals):
        self.string = _str
        self.vals = vals
    def print(self):
        params = re.findall(TokenType.PARAMALL.value, self.string)

        for i in range(len(params)):
            val = self.vals[i]
            self.string = self.string.replace(params[i], str(val.getValue()))
        print(self.string)

        #print(str(self.value.getValue()))


class Emtrix():
    def __init__(self):
        self.variables = []
        self.prints = []
        pass
    def __str__(self) -> str:
        _str = ''
        for i in range(len(self.variables)):
            _str += str(self.variables[i])

            if (i < len(self.variables) -1):
                _str += '\n'
        return _str
    def addPrint(self, _print):
        self.prints.append(_print)

    def printAll(self):
        for x in self.prints:
            x.print()
    def printVariables(self):
        print(self.__str__())
    def addVariable(self, value):
        var = self.__find__(value.name)

        if (var == None):
            self.variables.append(value)
        else:
            index = self.variables.index(var)
            self.variables[index] = value
    def getVariable(self, name):
        var = self.__find__(name)
        if (var == None):
            raise Exception("Cannot find the variable with name " + name)
        return var
    def containsVariable(self, name):
        var = self.__find__(name)
        return var != None

    def __find__(self, name):
        predicate = lambda x: x.name == name
        for var in self.variables:
            if (predicate(var)):
                return var
        return None
    